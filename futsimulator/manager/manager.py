from collections import deque, defaultdict
from futsimulator.positions.position import StatusOrder, SideOrder, Position
from futsimulator.stats.stats import statsPositions
from futsimulator.positions.orders import LimitStopOrder
import pdb

OPP_ORDER = {SideOrder.buy:SideOrder.sell, SideOrder.sell:SideOrder.buy}
OPP_POS = {SideOrder.buy:SideOrder.sell, SideOrder.sell:SideOrder.buy}

class PositionManager():

    def __init__(
        self, snapshot, max_size,
        commission_cfg, indicators = {}
        ):

        self.open_pos = deque()
        self.limit_ords = deque()
        self.stop_ords = deque()
        self.cl_pos = defaultdict(list)
        self.max_size = max_size
        self.com_cfg = commission_cfg
        self.snapshot = snapshot
        self.id_counter = 1
        self.indicators = indicators
        self.update()

    def update(self):
        """
        Update all the orders by verifying if any stop loss
        or take profit has been reached. It that is the case,
        then an open position will be moved to a closed position.
        """
        # Check if any limit orders needs to be executed
        self.check_limit_ords()
        # Check if any stop order needs to be executed
        self.check_stop_ords()

        open_pos_ = deque()
        while self.open_pos:
            pos = self.open_pos.popleft()
            pos.update_tick()
            if pos.status == StatusOrder.closed:
                self.cl_pos[pos.id_order].append(pos)
            else:
                open_pos_.append(pos)

        self.open_pos = open_pos_
        if self.indicators:
            for key, ind in self.indicators.items():
                ind.update(self)

    def delete_ls_order(self, id_order):
        """
        Removes a stop or limit order from the list of 
        orders that are in the queue
        """
        limit_ords_ = deque()
        while self.limit_ords:
            order = self.limit_ords.popleft()
            if order.id_counter != id_order:
                limit_ords_.append(order)
        self.limit_ords = limit_ords_
        
        stop_ords_ = deque()
        while self.stop_ords:
            order = self.stop_ords.popleft()
            if order.id_counter != id_order:
                stop_ords_.append(order)
        self.stop_ords = stop_ords_

    def modify_market_order(
            self, id_order, tp = None, sl = None
            ):
        """
        Updates a market order with its take profit
        or stop loss
        """
        open_pos_ = deque()
        while self.open_pos:
            order = self.open_pos.popleft()
            if order.id_order == id_order:
                if tp:
                    order.tp = tp
                if sl:
                    order.sl = sl

            open_pos_.append(order)

        self.open_pos = open_pos_
        self.update()

    def modify_ls_order(
            self, id_order, price = None,
            size = None, tp = None, sl = None
            ):
        """
        Updates a stop or limit order with its take profit
        or stoploss
        """
        limit_ords_ = deque()
        while self.limit_ords:
            order = self.limit_ords.popleft()
            if order.id_counter == id_order:
                if tp:
                    order.tp = tp
                if sl:
                    order.sl = sl
                if price:
                    order.price = price
                if size:
                    order.size = size

            limit_ords_.append(order)

        self.limit_ords = limit_ords_
        
        stop_ords_ = deque()
        while self.stop_ords:
            order = self.stop_ords.popleft()
            if order.id_counter == id_order:
                if tp:
                    order.tp = tp
                if sl:
                    order.sl = sl
            stop_ords_.append(order)
        self.stop_ords = stop_ords_
        self.update()

    def check_limit_ords(self):
        """
        Executes limit orders in the queue of limit orders
        when they satisfy their conditions
        """
        limit_ords_ = deque()
        while self.limit_ords:

            lo = self.limit_ords.popleft()
            method_queue = getattr(self.snapshot, "exec_order_by_queue", None)
            #pdb.set_trace()
            if lo.side == SideOrder.buy:
            
                if method_queue and self.snapshot.exec_order_by_queue(lo):
                    self.send_market_order(lo.side, lo.size, lo.tp, lo.sl)
                
                elif self.snapshot.ask <= lo.price:
                    self.send_market_order(lo.side, lo.size, lo.tp, lo.sl)
                
                else:
                    limit_ords_.append(lo)
            
            elif lo.side == SideOrder.sell:
                
                if method_queue and self.snapshot.exec_order_by_queue(lo):
                    self.send_market_order(lo.side, lo.size, lo.tp, lo.sl)
                
                elif self.snapshot.bid >= lo.price:
                    self.send_market_order(lo.side, lo.size, lo.tp, lo.sl)
                
                else:
                    limit_ords_.append(lo)
        
        self.limit_ords = limit_ords_

    def check_stop_ords(self):
        """
        Executes stop orders in the queue of stop orders
        when they satisfy their conditions.
        """
        stop_ords_ = deque()
        while self.stop_ords:
            so = self.stop_ords.popleft()
            if so.side == SideOrder.buy:
                if self.snapshot.ask >= so.price:
                    self.send_market_order(so.side, so.size, so.tp, so.sl)
                else:
                    stop_ords_.append(so)
            elif so.side == SideOrder.sell:
                if self.snapshot.bid <= so.price:
                    self.send_market_order(so.side, so.size, so.tp, so.sl)
                else:
                    stop_ords_.append(so)
        self.stop_ords = stop_ords_

    def send_limit_order(self, price, side, size, tp = None, sl = None):
        """
        Sends a limit order
        """
        
        lo = LimitStopOrder(price, side, size, tp, sl, self.id_counter)
        self.limit_ords.append(lo)
        self.id_counter += 1
        self.update()

    def send_stop_order(self, price, side, size, tp = None, sl = None):
        """
        Sends a stop order
        """
        so = LimitStopOrder(price, side, size, tp, sl, self.id_counter)
        self.stop_ords.append(so)
        self.id_counter += 1
        self.update()

    def send_market_order(
            self, side: str, size: float,
            tp: float = None, sl: float = None
        ) -> None:

        """
        First filter the orders that are more than allowed in 
        the configuration
        """
        info = self.get_infos()

        if side == None:
            if size > self.max_size:
                return
        elif side == info['open_orders']['side']:
            if info['open_orders']['total_size'] + size > self.max_size:
                return
        else:
            if size - info['open_orders']['total_size'] > self.max_size:
                return

        """
        Send a market order
        """
        self.update()
        if size <= 0:
            return

        open_pos_ = deque()

        """
        recent position is cleaned everytime
        we receive a new set of orders
        """
        while self.open_pos:

            pos = self.open_pos.popleft()

            if size ==0 or pos.side == side: # why size == 0 ? can we remove such condition ? 
                """
                If order is the same side, then just append
                a new one from the same side
                """
                open_pos_.append(pos)

            elif pos.side == OPP_ORDER[side]:
                """
                Check if we should close a set
                of positions because we received an opposite
                order for the current opened positions.
                """

                # If size of the order is less than current opened positions
                # then close that size of positions
                if pos.size - size >= 0:
                    """
                    Compute the amount that will be closed
                    and add it to the stack of closed
                    positions and the stack of recent closed
                    positions
                    """
                    remain = pos.size - size
                    pos.size = size
                    pos.close_order()
                    self.cl_pos[pos.id_order].append(pos)

                    if remain:
                        pos = Position(
                            self.snapshot, pos.side, remain,
                            pos.tp, pos.sl, self.com_cfg,
                            pos.id_order, pos.o_price, pos.o_time
                            )
                        pos.update_tick()
                        open_pos_.append(pos)
                        self.id_counter += 1
                    #Size is zero because we filled all requested
                    size = 0

                # If size of the order is more than current opened positions
                # then close that batch of positions, and recalculate the
                # remaining size of orders to process
                elif pos.size - size < 0 :
                    """
                    Set the total position that will be closed
                    and add it to the stack of recent closed.
                    """
                    pos.close_order()
                    self.cl_pos[pos.id_order].append(pos)

                    """
                    Update size to be filled for next position to be 
                    analysed
                    """
                    size -= pos.size

        if size > 0:
            pos = Position(
                self.snapshot, side, size,
                tp, sl, commission_cfg = self.com_cfg,
                id_order = self.id_counter
                )
            pos.update_tick()
            open_pos_.append(pos)
            self.id_counter +=1

        self.open_pos = open_pos_
        self.update()
        

    def liquidate(self) -> None:
        """
        Liquidates all the opened orders
        """
        opp_orders = []
        for pos in self.open_pos:
            side = OPP_ORDER[pos.side] 
            size = pos.size
            opp_orders.append((side,size))
        for op_ord in opp_orders:
            side, size = op_ord
            self.send_market_order(side, size)

    def cancel_all(self):
        """
        Cancels all the limit or stop orders
        """
        self.stop_ords = deque()
        self.limit_ords = deque()


    def get_infos(self):
        """
        Provide information about all the different 
        orders (opened or closed).
        """
        info_open = self._trads_info_open()
        info_close = self._trads_info_close()
        info_limit_stops = self._trads_info_limit_stop()
        infos = {
            "open_orders":vars(info_open),
            "closed_orders": info_close
            }
        infos.update(info_limit_stops)
        
        return infos

    def _trads_info_open(self):
        """
        Summarizes the trades information for
        the open trades :
        like the open profit and loss
        for any position that remain in the open position.
        """
        b_s = statsPositions.o_summarize(self.open_pos)

        return b_s

    def _trads_info_close(self):
        """
        Summarizes the trades information for
        the close trades containing the same trade id
        """
        data = {}
        for k_id, pos in self.cl_pos.items():
            b_s = statsPositions.c_summarize(pos)
            data[k_id] = vars(b_s)
        return data
    
    def _trads_info_limit_stop(self):
        """
        Provides information about the stop orders
        and limit orders that are opened.
        """
        data = {
            "stop_orders":[],
            "limit_orders":[]
            }
        for pos in self.stop_ords:
            data["stop_orders"].append(vars(pos))
        for pos in self.limit_ords:
            data["limit_orders"].append(vars(pos))
        return data