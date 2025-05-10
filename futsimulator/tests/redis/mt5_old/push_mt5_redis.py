import os
import csv
from tqdm import tqdm
import json
from datetime import datetime

from tradingrl.preproc.mt5          import load_data
from futsimulator.interfaces.redisinjectors import InjectStr2List
from futsimulator.interfaces.redisinjectors import InjectZadd

path_series = '/home/mora/Documents/projects/dataseries/mt5/EP/'

files = [
    "EP_202411010000_202411012059.csv"
]

stock_srs = load_data(os.path.join(path_series, files[0]))

data = stock_srs.to_dict(orient = 'records')
host_redis = '192.168.1.48'
port_redis = 6379
list_name_redis = 'EP_20241101_test'
list_name_idx = 'EP_20241101_test_idx'

r_inj = InjectStr2List(host_redis, port_redis)
r_inj_idx = InjectZadd(host_redis, port_redis)

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