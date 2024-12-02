from futsimulator.market.redissnapshots import TBBOSnapshot
from futsimulator.indicators.profile import VolumeProfile
from futsimulator.interfaces.redisindex import IndexDateDay
from datetime import datetime
import pytz
import pdb
import numpy as np

"""
VOLUME PROFILE INDICATOR
This test is to check the TBBOSnapshot class
when including the VolumeProfile class (indicator).
"""

host = '192.168.1.48'
port = 6379
list = 'UB_20240331'
decimal = 1e9
profile = VolumeProfile(10,10,1/32)
indicators = {'profile': profile}

start_time_preload = datetime(year=2024, month=3, day=31, hour = 22, minute = 0, tzinfo = pytz.utc)
start_time = datetime(year=2024, month=3, day=31, hour = 22, minute = 30, tzinfo = pytz.utc)
end_time = datetime(year=2024, month=3, day=31, hour = 23, minute=1, tzinfo = pytz.utc)

idx_date_day = IndexDateDay(
    prefix = 'UB', suffix = 'zadd',
    host = host, port = port
    )

print("Printing snapshot")
snapshot = TBBOSnapshot(host, port, decimal = decimal, idx_date_day= idx_date_day,
                        start_time = start_time, end_time = end_time, indicators=indicators,
                        start_time_preload= start_time_preload)

print(snapshot)
print('End of printing snapshot\n\n')

print("Printing Volume Profile")
print(snapshot.indicators['profile'])
for k in range(500):
    snapshot.update()
print(snapshot.indicators['profile'])
prf = snapshot.indicators['profile'].profile
print("Accessing the volume profile data")

val_dic = [val for key, val in prf.items()]
val = np.array(val_dic)
print(val.shape)