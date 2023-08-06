from pathlib import Path
import os
from typing import Dict
import hickle
import re
from typing import Dict, Union

import asyncio
from concurrent.futures import ProcessPoolExecutor

from rolling_window.helpers import make_async

class Peristance:

    
    @make_async
    def save(self,data_dict:Dict, path: str, id: str)-> None:
        pp = Path(path)
        if (pp.exists() is False or pp.is_dir() is False):
            pp.mkdir(parents=True, exist_ok=True)
        
        with open('%s/%s.hkl'%(path,id), 'w') as fi:
            hickle.dump(data_dict[id], fi)

    def load_all(self,path:str) -> Dict:
        data_dict = {}
        for datafile in filter(lambda x: x.endswith('.hkl'), os.listdir(path) ):
            id = re.sub('\.hkl$', '', datafile)
            data_dict[id] = hickle.load(datafile)

        return data_dict

    def load(self,id:str,data_dict:dict,path:str) -> Union[Dict,None]:
        os.chdir(path)
        try:
            with open('%s/%s.hkl'%(path,id), 'r') as fi:
                data_dict[id] = hickle.load(datafile)
            return data_dict[id]
        except:
            raise OSError('Missing data file for given id')




    

