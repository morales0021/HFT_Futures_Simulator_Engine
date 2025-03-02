
import os
import pdb
import pandas as pd
from tqdm import tqdm
import redis
import json
from tradingrl.preproc.mt5 import load_data, agregate_mt5, get_datetime_data
from datetime import datetime
from futsimulator.interfaces.redisinjectors import InjectStr2List
from futsimulator.interfaces.redisinjectors import InjectZadd

class MT5RedisReader:

    def __init__(
            self,
            host_redis: str,
            port_redis: int,
            identifier: str = None
            ):
        
        self.host_redis = host_redis
        self.port_redis = port_redis
        self.identifier = identifier
        self.datalist = []
        self.r = redis.Redis(host = self.host_redis, port = self.port_redis)
        self.r.ping()


    def load_data(
            self,
            path: str,
            files: list,
            agregate = True
            ):
        
        for file in files:
            try:
                df = load_data(os.path.join(path, file))
                if agregate:
                    df = agregate_mt5(df)
                self.inject_data(df)
            except Exception as e:
                print(f'Error with {file}: {e}')

    def get_list_name(self, dt):
        """
        Set list name for redis.
        """
        list_name_redis = f'{self.identifier}_{dt["year"]}{dt["month"]:02}{dt["day"]:02}_data'
        list_name_idx = f'{self.identifier}_{dt["year"]}{dt["month"]:02}{dt["day"]:02}_idx'
        return list_name_redis, list_name_idx

    def inject_data(self, df):
        """
        Injects data into redis.
        """
        dt = get_datetime_data(df)
        list_name_redis, list_name_idx = self.get_list_name(dt)

        self.datalist.append({
            "list_name_redis":list_name_redis,
            "list_name_idx":list_name_idx,
            "datetime":dt
        })

        r_inj = InjectStr2List(self.host_redis, self.port_redis)
        r_inj_idx = InjectZadd(self.host_redis, self.port_redis)
        data = df.to_dict(orient = 'records')

        for idx, element in tqdm(enumerate(data)):

            element['datetime'] = element['datetime'].timestamp()*1000

            if element['flags'] == 88 :
                element["side"] = 's'
            elif element['flags'] == 56:
                element["side"] = 'b'
            else:
                element["side"] = 'unknown'
            element.pop('flags')
            element['volume'] = abs(element['volume'])

            r_inj.inject(list_name_redis,json.dumps(element))

            score = int(element['datetime'])
            data = {idx:score}
            r_inj_idx.inject(list_name_idx,data)

        print("Data injected for ", list_name_redis)


    def bind_datalist_by_datetime(self, start_time: datetime, end_time: datetime):
        """
        Bind the data list with the indexes.
        """
        lst_name, lst_idx_name = self.get_list_name(
            {"year":start_time.year,
             "month":start_time.month,
             "day":start_time.day
             }
        )

        if not self.r.exists(lst_name):
            raise Exception(f"List {lst_name} does not exist")

        if not self.r.exists(lst_idx_name):
            raise Exception(f"List {lst_idx_name} does not exist")
        
        idx_start,  idx_end, lst_idx_name = self._locate_time_index(
            lst_idx_name, start_time, end_time
        )

        return idx_start, idx_end, lst_name, lst_idx_name

    def _locate_time_index(self, lst_idx_name, start_time, end_time):

        start = start_time.timestamp()*1000
        end = end_time.timestamp()*1000
        s_idxs = self.r.zrangebyscore(
            lst_idx_name, min = start, max = end,
            start = 0, num = 2)
        
        e_idxs = self.r.zrevrangebyscore(
            lst_idx_name, max = end, min = start,
            start = 0, num = 2)
        
        return int(s_idxs[0]), int(e_idxs[0]), lst_idx_name
