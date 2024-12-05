
import json
from datetime import datetime
from futsimulator.interfaces.redislist import RedisList

class MT5:

    def __init__(self, data: bytes | str, symbol: str = None) -> None:

        if isinstance(data, bytes):
            data = data.decode('utf-8')
            dict_d = json.loads(data)
        elif isinstance(data, str):
            dict_d = json.loads(data)
        elif isinstance(data, dict):
            dict_d = data

        self._load_attr(dict_d)
        self.symbol = symbol

    def _load_attr(self, dict_d: dict) -> None:
        self.ts = int(dict_d['datetime'])/1e3
        self.time = self.ts
        self.datetime = datetime.utcfromtimestamp(self.ts)
        self.side = dict_d["side"]
        self.price = float(dict_d["close"])
        self.size = dict_d["volume"]
        self.ask = float(dict_d["ask"])
        self.bid = float(dict_d["bid"])