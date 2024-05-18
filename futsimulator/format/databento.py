
import json
from datetime import datetime
from futsimulator.interfaces.redislist import RedisList

class TBBO:

    def __init__(self, data: bytes | str, decimal: float):

        if isinstance(data, bytes):
            data = data.decode('utf-8')
            dict_d = json.loads(data)
        elif isinstance(data, str):
            dict_d = json.loads(data)
        elif isinstance(data, dict):
            dict_d = data

        self.decimal = decimal    
        self._load_attr(dict_d)


    def _load_attr(self, dict_d: dict) -> None:

        self.ts = int(dict_d['ts_recv'])/1e9
        self.time = self.ts
        self.datetime = datetime.utcfromtimestamp(self.ts)
        self.side = dict_d["side"]
        self.price = float(dict_d["price"]) / self.decimal
        self.size = dict_d["size"]
        self.ask = float(dict_d["levels"][0]["ask_px"]) / self.decimal
        self.bid = float(dict_d["levels"][0]["bid_px"]) / self.decimal
        self.ask_sz_0 = dict_d["levels"][0]["ask_sz"]
        self.bid_sz_0 = dict_d["levels"][0]["bid_sz"]
        self.symbol = dict_d['symbol']