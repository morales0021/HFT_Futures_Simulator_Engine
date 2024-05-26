import redis
from datetime import datetime

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
        name_list = self.prefix + '_' + start_time.strftime("%Y%m%d") 
        name_idx = name_list + '_' + self.suffix

        start = start_time.timestamp()*1e9
        end = end_time.timestamp()*1e9

        s_idxs = self.r.zrangebyscore(
            name_idx, min = start, max = end,
            start = 0, num = 2)
        
        e_idxs = self.r.zrevrangebyscore(
            name_idx, max = end, min = start,
            start = 0, num = 2)
        
        return int(s_idxs[0]), int(e_idxs[0]), name_list, name_idx