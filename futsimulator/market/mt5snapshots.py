import textwrap
from datetime import datetime
from futsimulator.format.metatrader import MT5
from futsimulator.interfaces.redislist import RedisList
from futsimulator.market.snapshots import MarketSnapshot
from futsimulator.positions.position import SideOrder
import math
import warnings
import pdb

class MT5Snapshot(MarketSnapshot):

    def __init__(self, host, port, symbol: str = '', idx_date_day = None,
                 start_time: datetime = None, end_time: datetime = None,
                 start_time_preload: datetime = None
                 ):
        """
        Reads a list from redis containing price data having a 
        MT5 format and reformat its information as
        attributes.
        Note that if idx_date_day is provided, then is required start_time and
        end_time.
        """
        if idx_date_day:
            if start_time_preload:
                idx_start, max_idx, list_name, _ = idx_date_day.get_indexes(start_time_preload, end_time)
                idx_half, _,_,_ = idx_date_day.get_indexes(start_time, end_time)
            else:
                idx_start, max_idx, list_name, _ = idx_date_day.get_indexes(start_time, end_time)

        self.rl = RedisList(host, port, list_name, idx = idx_start, max_idx = max_idx)
        self.init_price = None
        self.finished = False
        self.symbol = symbol
        self.update()

        if idx_half:
            while self.idx <= idx_half:
                self.update()

    def update(self):
        """
        Generates the attributes by by reading the price information from
        redis. 
        """
        try:
            self.snap = MT5(self.rl.read(), self.symbol)
            self.idx = self.rl.idx

            if not self.init_price:
                self.init_price = self.snap.price

        except Exception:
            warnings.warn(
                f"""Redis list returned none at index {self.idx},"""
                """ possibly because its finished""")
            self.finished = True
            return

    def __getattr__(self, attr):

        try:
            return getattr(self.snap, attr)
        except AttributeError as e:
            raise AttributeError("Attribute not found in MT5Snapshot")

    def update_queue(self, limit_order):
        """
        Updates the queue of a limit order by following a mecanic
        as precised by the Sierra Chart Software.
        """
        raise NotImplemented("Method not supported for MT5Snapshot")
    
    
    def __str__(self):

        cls_info = f"""
        bid: {self.bid},
        ask: {self.ask},
        time: {self.time},
        datetime: {self.datetime},
        side: {self.side},
        size: {self.size},
        last: {self.price}
        symbol: {self.symbol},
        idx: {self.idx}
        """

        return textwrap.dedent(cls_info)