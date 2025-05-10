import redis

class InjectStr2List:
    """
    Injects data into a list
    """
    def __init__(self, host, port):

        self.r = redis.Redis(host = host, port = port)
        self.r.ping()
        
    def inject(self, lst_name, data):
        
        self.r.rpush(lst_name, data)


class InjectZadd:
    """
    Injects data into a sorted set.
    """

    def __init__(self, host, port):

        self.r = redis.Redis(host = host, port = port)
        self.r.ping()
        
    def inject(self, lst_name, data):
        
        self.r.zadd(lst_name, data)