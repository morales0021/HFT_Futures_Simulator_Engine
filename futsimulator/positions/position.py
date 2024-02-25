import pdb
from enum import Enum
import textwrap
from futsimulator.comm.commission import commission
from futsimulator.market.snapshots import MarketSnapshot

class StatusOrder(Enum):
    opened = 1
    closed = 2

class SideOrder(Enum):
    buy = 1
    sell = 2

class Position:

    def __init__(
        self, snapshot: MarketSnapshot, side: SideOrder, size: float,
        tp: float  = None, sl: float = None, commission_cfg: dict = {}):
        """
        A position is opened at the moment that we instantiate such position
        """

        assert(isinstance(size,(int, float)))
        assert(isinstance(commission_cfg, dict))

        """
        Creates an instance for opening a new position
        """
        if side == SideOrder.buy:
            o_price = snapshot.ask
        else:
            o_price = snapshot.bid
        
        self.snapshot = snapshot

        # open price
        self.o_price = o_price
        # open time
        self.o_time = snapshot.time
        # side order (buy or sell)
        self.side = side
        # the symbol
        self.symbol = snapshot.symbol

        # take profit
        self.tp = tp
        # stoploss
        self.sl = sl
        # size of the position
        self.size = size
        
        # status set if the order is opened or closed
        self.status = StatusOrder.opened

        # commission object
        self.com_fun = commission(commission_cfg)

        # the open profit and loss, initialize by asking commission
        self.o_pnl = self.com_fun.get_com(0.0,self.o_price)*self.size
        # the closed profit
        self.cl_pnl = None
        # closing price
        self.cl_price = None
        # close time
        self.cl_time = None

        # the delta time computes the time of the order since its inception
        self.delta_t = 0

        # check if close by take profit and stop loss

        self._check_tp()
        print(self.o_pnl)
        self._check_sl()

    def update_tick(self) -> None:
        """
        Updates the status from a position
        """
        # check first take profit and stop loss
        self._delta_time()
        self._check_tp()
        self._check_sl()
        # update open profit and loss if still opened
        self._op_profit()

    def update_tp_sl(self, tp_sl_data: dict) -> None:
        """
        Update the take profit and stoploss, we use the 
        last tick received in cache.
        """
        if self.status == StatusOrder.opened:
            self.tp = tp_sl_data['tp']
            self.sl = tp_sl_data['sl']
            self._check_tp(self.snapshot)
            self._check_sl(self.snapshot)

    def close_order(self):
        """
        Close the order and computes the closed profit and loss
        It uses the last market snapshot that was provided.
        """
        if self.status == StatusOrder.opened:
            if self.side == SideOrder.buy:
                pnl = (self.snapshot.bid - self.o_price)
                self.cl_pnl = self.com_fun.get_com(pnl, self.o_price)*self.size
            else:
                pnl =  (self.o_price - self.snapshot.ask)
                self.cl_pnl = self.com_fun.get_com(pnl, self.o_price)*self.size

    def _check_tp(self):
        """
        Close an order if the takeprofit is satisfied
        """

        if not self.tp or self.status == StatusOrder.closed:
            return
        elif self.side == SideOrder.buy and self.tp <= self.snapshot.bid:
            # Close the position
            self.o_pnl = None
            self.cl_price = self.tp
            self.close_order()
            self.cl_time = self.snapshot.time
            self.status = StatusOrder.closed

        elif self.side == SideOrder.sell and self.tp >= self.snapshot.ask:
            # Close the position
            self.o_pnl = None
            self.cl_price = self.tp
            self.close_order()
            self.cl_time = self.snapshot.time
            self.status = StatusOrder.closed
    
    def _check_sl(self):
        """
        Close an order if the stop loss is satisfied
        """
        if not self.sl or self.status == StatusOrder.closed:
            return
        elif self.side == SideOrder.buy and self.sl >= self.snapshot.bid:
            # Close the position
            self.o_pnl = None
            self.cl_price = self.sl
            self.close_order()
            self.cl_time = self.snapshot.time
            self.status = StatusOrder.closed

        elif self.side == SideOrder.sell and self.sl <= self.snapshot.ask:
            # Close the position
            self.o_pnl = None
            self.cl_price = self.sl
            self.close_order()
            self.cl_time = self.snapshot.time
            self.status = StatusOrder.closed

    def _delta_time(self):
        """
        Updates the attribute delta_time in the position
        delta_time provides the live of the current trade
        """
        if self.status == StatusOrder.opened:
            self.delta_t = self.snapshot.time - self.o_time

    def _op_profit(self):
        """
        Updates the open profit and loss if the order
        is still opened
        """
        if self.status == StatusOrder.opened:
            if self.side == SideOrder.buy:
                pnl = (self.snapshot.bid - self.o_price)
                self.o_pnl = self.com_fun.get_com(pnl,self.o_price)*self.size
            else:
                pnl = (self.o_price - self.snapshot.ask)
                self.o_pnl = self.com_fun.get_com(pnl,self.o_price)*self.size

    def __str__(self):

        cls_info = f"""
        ----POSITION ------
        symbol: {self.symbol},
        position type: {self.side},
        order status: {self.status},
        position size: {self.size},
        time alive: {self.delta_t}
        ----open-----
        open price: {self.o_price},
        open time: {self.o_time},
        open profit: {self.o_pnl},
        take profit: {self.tp},
        stop loss: {self.sl},
        ----close-----
        closed profit: {self.cl_pnl},
        closed price: {self.cl_price}
        ----market----
        ask: {self.snapshot.ask}
        bid: {self.snapshot.bid}
        """

        return textwrap.dedent(cls_info)