import redis
from datetime import datetime
import pytz
import pdb


class IndexDateDay:

    def __init__(self, prefix, suffix, host, port):

        self.prefix = prefix
        self.suffix = suffix
        self.r = redis.Redis(host = host, port = port)
        self.r.ping()

    def get_indexes(self, start_time: datetime, end_time: datetime)-> tuple[int, int]:
        """
        Provides the start index and end index for a given historical
        price data stored in redis. This class requires that the 
        historical index data is already stored in the redis cluster.
        """
        name_idx = self.prefix + '_' + start_time.strftime("%Y%m%d") + '_' + self.suffix

        start = start_time.timestamp()*1e9
        end = end_time.timestamp()*1e9
        s_idxs = self.r.zrangebyscore(
            name_idx, min = start, max = end,
            start = 0, num = 2)
        
        e_idxs = self.r.zrevrangebyscore(
            name_idx, max = end, min = start,
            start = 0, num = 2)
        
        return int(s_idxs[0]), int(e_idxs[0])



host = '192.168.1.48'
port = 6379
list_name_redis = 'UB_20240331_zadd'
r = redis.Redis(host = host, port = port)
max_n = 10
start = datetime(year=2024, month=3, day=31, hour = 22, minute = 1, tzinfo = pytz.utc)
start = start.timestamp()*1e9

end = datetime(year=2024, month=3, day=31, hour = 22, minute=5, tzinfo = pytz.utc)
end = end.timestamp()*1e9
end = '('+str(end)

vals = r.zrevrangebyscore(list_name_redis, min = start, max = end, start = 0, num = 10)
print(vals)


start = datetime(year=2024, month=3, day=31, hour = 22, minute = 0, tzinfo = pytz.utc)
end = datetime(year=2024, month=3, day=31, hour = 23, minute=1, tzinfo = pytz.utc)
idxdd = IndexDateDay("UB", "zadd", host, port)
vals = idxdd.get_indexes(start, end)
print(vals)