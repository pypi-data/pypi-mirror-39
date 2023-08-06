from typing import NewType, Union, Dict
import numpy as np
from dataclasses import dataclass
from operator import itemgetter
import os
import datetime
import glob
from rolling_window.peristance import Peristance


@dataclass
class WindowOptions:
    """
    Parameters
    ----------
    period: this is the total size in rolling window in seconds - used in all window options
    step: the jump between windows used in the hopping window option
    """
    period: datetime.timedelta  
    step: datetime.timedelta 


class RollingWindow(Peristance):
    def __init__(
        self,
        *,
        window_type: str,
        datastructure: any,
        sort: bool = False,
        persistance: bool = False,
        path: str = os.getcwd() + "/store",
        window_options: WindowOptions
    ):
        super().__init__()
        self._window_types = ["sliding", "hopping", "batch"]  # use enum - note here to remind me to change this to use enums
        self.window_type = window_type
        self.window_options = window_options
        if not self._check_window_option():
            raise AttributeError(
                "The window type must be either 'sliding', 'hopping' or 'batch "
            )
        self.persistance = persistance
        self.sort = sort
        self.path = path
        self.options = window_options
        self.type_window = window_type
        self.annotations = datastructure.__annotations__
        if "time" not in self.annotations.keys():
            raise AttributeError(
                "datastructure must contain a field called time that accepts the unix-time of the data of type float"
            )
        self.datastructure_map = {
            key: ii for ii, key in enumerate(sorted(self.annotations.keys()), 1)
        }
        self.datastructure_map["time"] = 0
        self.dtype = [
            (key, self.annotations[key])
            for key, index in sorted(self.datastructure_map.items(), key=itemgetter(1))
        ]
        self.data_dict = {}

        

    async def add_data(
        self, id: str, data: any
    ) -> None:  
        if id not in set(self.data_dict.keys()):  # check the in memory database first
            if (
                len(glob.glob(id + ".hkl")) > 0
            ):  
                try:
                    self.data_dict = self.load(
                        id=id, data_dict=self.data_dict, path=self.path
                    )  
                except OSError:
                    pass
        new_data = data.__dict__
        new_data_array = [0] * (len(new_data))
        for key, value in new_data.items():
            new_data_array[self.datastructure_map[key]] = value
        try:
            self.data_dict[id] = np.vstack(
                [
                    self.data_dict[id],
                    np.array([tuple(new_data_array)], dtype=self.dtype),
                ]
            )
        except:
            self.data_dict[id] = np.array([tuple(new_data_array)], dtype=self.dtype)

        if self.persistance is True:
            await self.save(id)

    async def save(self, id):
        await super(RollingWindow, self).save(
            **{"data_dict": self.data_dict, "path": self.path, "id": id}
        )

    def send(self, id: str) -> Union[np.ndarray, None]:
        if self.sort is True:
            self._sort_data(id)  # make sure everything is in time order

        if self.window_type is "sliding":
            return self._sliding_filter(id)
        elif self.window_type is "hopping":
            return self._hopping_filter(id)
        elif self.window_type is "batch":
            return self._batch_filter(id)

    def _sliding_filter(self, id):
        """Send the data for every time step when the amount of data in the window spans the specified time period"""
        if (
            self.data_dict[id]["time"][-1] - self.data_dict[id]["time"][0]
        ) >= self.window_options.period.seconds:
            to_return = self.data_dict[id]
            self.data_dict[id] = self.data_dict[id][1:]
            return to_return

    def _hopping_filter(self, id):
        """"The hopping window hops by a given time frame every couple of seconds"""
        if (
            self.data_dict[id]["time"][-1] - self.data_dict[id]["time"][0]
        ) >= self.window_options.period.seconds:
            boundary = (
                self.data_dict[id]["time"][0][0] + self.window_options.step.seconds
            )
            to_return = self.data_dict[id]
            sliced_array = self.data_dict[id][self.data_dict[id]["time"] >= boundary]
            self.data_dict[id] = sliced_array.reshape(np.shape(sliced_array)[0], 1)
            return to_return

    def _batch_filter(self, id):
        if (
            self.data_dict[id]["time"][-1] - self.data_dict[id]["time"][0]
        ) >= self.window_options.period.seconds:
            to_return = self.data_dict[id]
            self.data_dict[id] = self.data_dict[id][
                -1
            ]  # include the last value in the batch to provide continuity
            return to_return

    def get_ids(self):
        return self.data_dict.keys()

    def _map_dataclass(self, dataclass_object):
        pass

    def _check_window_option(self):
        return self.window_type in self._window_types

    def _sort_data(self, id):
        self.data_dict[id] = np.sort(self.data_dict[id], axis=0, order="time")
