import textwrap
from futsimulator.format.databento import TBBO
from futsimulator.interfaces.redislist import RedisList
from futsimulator.market.snapshots import MarketSnapshot
from futsimulator.positions.position import SideOrder
import pdb

class TBBOSnapshot(MarketSnapshot):

    def __init__(self, host, port, list_name, decimal, indicators = {}):
        """
        Reads a list from redis containing price data having a 
        databento format and reformat its information as
        attributes.
        """

        self.rl = RedisList(host, port ,list_name)
        self.decimal = decimal
        self.indicators = indicators
        self.update()

    def update(self):
        """
        Generates the attributes by by reading the price information from
        redis. 
        """
        self.snap = TBBO(self.rl.read(), self.decimal)
        self.idx = self.rl.idx

        """
        Updates all the indicators that were integrated into the snapshot
        instance.
        """
        if self.indicators:
            for key, ind in self.indicators.items():
                ind.update(self)

    def __getattr__(self, attr):

        try:
            return getattr(self.snap, attr)
        except AttributeError as e:
            raise AttributeError("Attribute not found in TBBO Class")

    def update_queue(self, limit_order):
        """
        Updates the queue of a limit order by following a mecanic
        as precised by the Sierra Chart Software.
        """
        if not limit_order.queue:
            if limit_order.side == SideOrder.buy and self.bid == limit_order.price:
                limit_order.queue = self.bid_sz_0 + limit_order.size
            elif limit_order.side == SideOrder.sell and self.ask == limit_order.price:
                limit_order.queue = self.ask_sz_0 + limit_order.size
            else:
                return
        else:
            if limit_order.side == SideOrder.buy and self.bid == limit_order.price:
                if self.side == 'A' and self.price == self.bid:  # A is Ask 
                    limit_order.queue -= self.size
                if limit_order.queue > self.bid_sz_0 + limit_order.size:
                    limit_order.queue = self.bid_sz_0 + limit_order.size
            
            if limit_order.side == SideOrder.sell and self.ask == limit_order.price:
                if self.side == 'B' and self.price == self.ask:
                    limit_order.queue -= self.size
                if limit_order.queue > self.ask_sz_0 + limit_order.size:
                    limit_order.queue = self.ask_sz_0 + limit_order.size
    
    def exec_order_by_queue(self, limit_order):
        """
        Checks if a limit order should be executed or not based on a 
        queuing system.
        """
        self.update_queue(limit_order)
        if limit_order.queue < 0:
            return True
        else:
            return False

    def __str__(self):

        cls_info = f"""
        bid: {self.bid},
        ask: {self.ask},
        time: {self.time},
        datetime: {self.datetime},
        side: {self.side},
        size: {self.size},
        last: {self.price}
        bid_sz_0: {self.bid_sz_0},
        ask_sz_0: {self.ask_sz_0},
        symbol: {self.symbol},
        idx: {self.idx}
        """

        return textwrap.dedent(cls_info)