from futsimulator.comm.commission import commission
from futsimulator.market.snapshot import marketSnapshot

class StatusOrder(Enum):
    opened = 1
    closed = 2

class SideOrder(Enum):
    buy = 1
    sell = 2

class position:

    def __init__(
        self, snapshot: marketSnapshot, side: SideOrder, size: float,
        tp: float  = None, sl: float = None, commission_cfg: dict = {}):
        """
        A position is opened at the moment that we instantiate such position
        """

        assert(isinstance(size,(int, float)))
        assert(isinstance(commission_cfg,dict))

        """
        Creates an instance for opening a new position
        """
        if side = SideOrder.buy:
            o_price = snapshot.ask
        else:
            o_price = snapshot.bid
        
        self.last_snapshot = snapshot

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
        # index alive
        self.index = 0

        # the delta time computes the time of the order since its inception
        self.delta_t = None

        # check if close by take profit and stop loss
        self._check_tp(snapshot)
        self._check_sl(snapshot)


    def update_tick(self, snapshot: marketSnapshot) -> None:
        """
        Updates the status from a position
        """
        # check first take profit and stop loss
        self._delta_time(snapshot)
        self._check_tp(snapshot)
        self._check_sl(snapshot)
        # update open profit and loss if still opened
        self.op_profit(self, snapshot.price_data())
        # Update last snapshot
        self.last_snapshot = snapshot

    def _check_tp(self, snapshot: marketSnapshot):
        """
        Close an order if the takeprofit is satisfied
        """
        if not self.tp or self.status == StatusOrder.closed:
            return
        elif side == 'b' and self.tp <= snapshot.bid:
            # Close the position
            self.o_pnl = None
            self.cl_price = self.tp
            self.cl_profit()
            self.cl_time = snapshot.time
            self.status = StatusOrder.closed

        elif side == 's' and self.tp >= snapshot.ask:
            # Close the position
            self.o_pnl = None
            self.cl_price = self.tp
            self.cl_profit()
            self.cl_time = snapshot.time
            self.status = StatusOrder.closed
    
    def _check_sl(self, snapshot: marketSnapshot):
        """
        Close an order if the stop loss is satisfied
        """
        if not self.sl or self.status == StatusOrder.closed:
            return
        elif side == 'b' and self.sl >= snapshot.ask:
            # Close the position
            self.o_pnl = None
            self.cl_price = self.sl
            self.cl_profit()
            self.cl_time = snapshot.time
            self.status = StatusOrder.closed

        elif side == 's' and self.sl <= snapshot.bid:
            # Close the position
            self.o_pnl = None
            self.cl_price = self.sl
            self.cl_profit()
            self.cl_time = snapshot.time
            self.status = StatusOrder.closed

    def _delta_time(self, snapshot: marketSnapshot):
        """
        Updates the attribute delta_time in the position
        delta_time provides the live of the current trade
        """
        if self.status == StatusOrder.opened:
            self.delta_t = snapshot.time - self.o_time

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
            if self.side == 'b':
                pnl = (self.last_snapshot.bid - self.o_price)
                self.cl_pnl = self.com_fun.get_com(pnl, self.o_price)*self.size
            else:
                pnl =  (self.o_price - self.last_snapshot.ask)
                self.cl_pnl = self.com_fun.get_com(pnl, self.o_price)*self.size

    def op_profit(self, snapshot: marketSnapshot):
        """
        Updates the open profit and loss if the order
        is still opened
        """
        if self.status == StatusOrder.opened:
            if self.side == 'b':
                pnl = (snapshot.bid - self.o_price)
                self.o_pnl = self.com_fun.get_com(pnl,self.o_price)*self.size
            else:
                pnl = (self.o_price - snapshot.ask)
                self.o_pnl = self.com_fun.get_com(pnl,self.o_price)*self.size