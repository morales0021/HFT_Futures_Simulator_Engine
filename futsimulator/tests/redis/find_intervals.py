import redis
from datetime import datetime
import pytz
import pdb

from futsimulator.interfaces.redisindex import IndexDateDay

host = '192.168.1.48'
port = 6379
# list_name_redis = 'UB_20240331_zadd'
# r = redis.Redis(host = host, port = port)
# max_n = 10
# start = datetime(year=2024, month=3, day=31, hour = 22, minute = 1, tzinfo = pytz.utc)
# start = start.timestamp()*1e9

# end = datetime(year=2024, month=3, day=31, hour = 22, minute=5, tzinfo = pytz.utc)
# end = end.timestamp()*1e9
# end = '('+str(end)

# vals = r.zrevrangebyscore(list_name_redis, min = start, max = end, start = 0, num = 10)
# print(vals)


start = datetime(year=2024, month=3, day=31, hour = 22, minute = 0, tzinfo = pytz.utc)
end = datetime(year=2024, month=3, day=31, hour = 23, minute=1, tzinfo = pytz.utc)
idxdd = IndexDateDay("UB", "zadd", host, port)
vals = idxdd.get_indexes(start, end)
print(vals)