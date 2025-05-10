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

    def __init__(
            self,
            host,
            port,
            symbol: str,
            mt5_reader,
            start_time: datetime,
            end_time: datetime
            ):
        """
        """
        try:
            idx_start, idx_end, list_name, lst_idx_name = mt5_reader.bind_datalist_by_datetime(
                start_time, end_time
            )

            print(f"idx_start: {idx_start}, idx_end: {idx_end}, list_name: {list_name}")
            self.list_name = list_name
            self.rl = RedisList(
                host,
                port,
                list_name,
                idx = idx_start,
                max_idx = idx_end
            )

            self.init_price = None
            self.finished = False
            self.symbol = symbol
            self.step()
        except Exception as e:
            print(f"Exception with {start_time}, {end_time}")

    def step(self):
        """
        Generates the attributes by by reading the price information from
        redis. 
        """
        try:

            self.snap = MT5(self.rl.read(), self.symbol)
            self.idx = self.rl.idx

            if not self.init_price:
                self.init_price = self.snap.price

        except Exception as e:
            print("Exception with ", self.list_name)
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