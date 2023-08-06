import sys, os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath)
from pathlib import Path

import asyncio

from dataclasses import dataclass

import pytest
import random
import time
import datetime
import numpy as np

import paco
from contextlib import ContextDecorator

from rolling_window.rolling_window import RollingWindow, WindowOptions

@dataclass
class PressureData:
    time: int
    pressure: float

def clean():
    path = os.getcwd() + '/store'
    for the_file in os.listdir(path):
        os.remove(path+'/%s'%(the_file))

class clean_dir(ContextDecorator):
    def __enter__(self):
        clean()
        
    def __exit__(self, *exc):
        clean()
    
    
@pytest.fixture
def hopping_window_peristance_sort():
    window_options = WindowOptions(period = datetime.timedelta(seconds=10),step=datetime.timedelta(seconds=2))
    window = RollingWindow(window_type = 'sliding', datastructure=PressureData, sort=True, persistance=True, window_options=window_options)
    return window

@pytest.fixture
def hopping_window_no_peristance_sort():
    window_options = WindowOptions(period = datetime.timedelta(seconds=10),step=datetime.timedelta(seconds=2))
    window = RollingWindow(window_type = 'hopping', datastructure=PressureData, sort=False, persistance=False, window_options=window_options)
    return window

def test_setup(hopping_window_peristance_sort):
    rolling_window = hopping_window_peristance_sort
    assert rolling_window.type_window == 'sliding'
    #assert dataclass_map ==

@pytest.fixture
def hopping_window_sliding():
    window_options = WindowOptions(period = datetime.timedelta(seconds=10),step=datetime.timedelta(seconds=2))
    window = RollingWindow(window_type = 'sliding', datastructure=PressureData, sort=False, persistance=False, window_options=window_options)
    return window

@pytest.fixture
def hopping_window_hopping():
    window_options = WindowOptions(period = datetime.timedelta(seconds=10),step=datetime.timedelta(seconds=2))
    window = RollingWindow(window_type = 'hopping', datastructure=PressureData, sort=False, persistance=False, window_options=window_options)
    return window

@pytest.fixture
def hopping_window_batch():
    window_options = WindowOptions(period = datetime.timedelta(seconds=10),step=datetime.timedelta(seconds=2))
    window = RollingWindow(window_type = 'batch', datastructure=PressureData, sort=False, persistance=True, window_options=window_options)
    return window

#@pytest.mark.usefixtures("clean_dir")
@clean_dir()
def test_add_data_wrapper(hopping_window_peristance_sort):
    async def test_add_data(hopping_window_peristance_sort):
        rolling_window = hopping_window_peristance_sort
        window_id = 'agentgo'
        N=3
        time_for_testing = [120, 500, 20]
        for ii in range(0,N):
            data = PressureData(time=time_for_testing[ii], pressure=round(random.uniform(2,20),2) )
            await rolling_window.add_data(id = window_id, data=data)
        data = rolling_window.send(window_id)
        array_size = np.shape(data)
        assert len(data[0][0]) == 2
        assert len(data) == N
        assert data[0]['time'][0]<data[array_size[0]-1]['time'][0]
    paco.run(test_add_data(hopping_window_peristance_sort))

#@pytest.mark.usefixtures("clean_dir")
@clean_dir()
def test_sliding_window_wrapper(hopping_window_sliding):
    async def test_sliding_window(hopping_window_sliding):
        rolling_window = hopping_window_sliding
        window_id = 'agentgoa'
        count = 0
        for ii in range(0,100):
            data = PressureData(time=ii, pressure=round(random.uniform(2,20),2) )
            await rolling_window.add_data(id = window_id, data=data)
            data_to_process = rolling_window.send(id=window_id)
            if data_to_process is not None:
                count +=1
                assert (data_to_process['time'][-1] - data_to_process['time'][0]) >= rolling_window.window_options.period.seconds
        assert count == 90 # because for the first 10 seconds it is filling the array, and for the remaining 90 seconds, it is sending data, every second
    paco.run(test_sliding_window(hopping_window_sliding))

#@pytest.mark.usefixtures("clean_dir")
@clean_dir()
def test_hopping_window_wrapper(hopping_window_hopping):
    async def test_hopping_window(hopping_window_hopping):
        rolling_window = hopping_window_hopping
        window_id = 'agentgoc'
        previous = -rolling_window.window_options.step.seconds
        for ii in range(0,100):
            data = PressureData(time=ii, pressure=round(random.uniform(2,20),2) )
            await rolling_window.add_data(id = window_id, data=data)
            data_to_process = rolling_window.send(window_id)
            if data_to_process is not None:
                assert (data_to_process['time'][0][0] - previous) >= rolling_window.window_options.step.seconds
                previous = data_to_process['time'][0][0]

    paco.run(test_hopping_window(hopping_window_hopping))

#@pytest.mark.usefixtures("clean_dir")
@clean_dir()
def test_batch_window_wrapper(hopping_window_batch):
    async def test_batch_window(hopping_window_batch):
        rolling_window = hopping_window_batch
        window_id= 'agentgoe'
        count = 0
        for ii in range(0,101):
            data = PressureData(time=ii, pressure=round(random.uniform(2,20),2) )
            await rolling_window.add_data(id = window_id, data=data)
            data_to_process = rolling_window.send(id=window_id)
            if data_to_process is not None:
                count+=1
        assert count == 10
    
    paco.run(test_batch_window(hopping_window_batch))

#@pytest.mark.usefixtures("clean_dir")
@clean_dir()
def test_load_data(hopping_window_batch):
    rolling_window = hopping_window_batch
    window_id= 'agentgoj'

    async def test_batch_window(hopping_window_batch): # hopping_window_batch has persistance = True
        for ii in range(0,100):
            data = PressureData(time=ii, pressure=round(random.uniform(2,20),2) )
            await rolling_window.add_data(id = window_id, data=data)
            rolling_window.send(id=window_id)

    paco.run(test_batch_window(hopping_window_batch)) 

    path = rolling_window.path
    path_object = Path(path+'/%s.hkl'%(window_id))
    assert path_object.is_file()
    rolling_window.data_dict = {} # not remove the internal data dictionary and check that it is now loaded from the file correctly
    paco.run(test_batch_window(hopping_window_batch)) 
    assert len(rolling_window.data_dict) != 0


# def clean_up(clean_dir):
#     pass
    