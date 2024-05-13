import redis

class RedisList:

    def __init__(self, host: str, port: int, name_list: str, idx: int = -1) -> None:

        self.host = host
        self.port = port
        self.r = redis.Redis(host = host, port = port)
        self.name_list = name_list
        self.len = self.r.llen(name_list)
        # Represents the index that will be provided in the next read
        self.idx = idx

    def read(self) -> bytes:
        self.idx += 1
        item = self.r.lrange(self.name_list, self.idx, self.idx)
        if not item:
            return None
        return item[0]