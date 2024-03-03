from collections import deque, defaultdict
from futsimulator.positions.position import StatusOrder, SideOrder, Position
from futsimulator.stats.stats import statsPositions
import pdb

OPP_ORDER = {SideOrder.buy:SideOrder.sell, SideOrder.sell:SideOrder.buy}
OPP_POS = {SideOrder.buy:SideOrder.sell, SideOrder.sell:SideOrder.buy}

class PositionManager():

    def __init__(
        self, snapshot, max_b_size, max_s_size,
        commission_cfg
        ):

        self.open_pos = deque()
        self.cl_pos = defaultdict(list)
        self.max_b_size = max_b_size
        self.max_s_size = max_s_size
        self.com_cfg = commission_cfg
        self.snapshot = snapshot
        self.id_counter = 1

    def update(self):
        """
        Update all the orders by verifying if any stop loss
        or take profit has been reached. It that is the case,
        then an open position will be moved to a closed position.
        """
        #pdb.set_trace()
        open_pos_ = deque()
        while self.open_pos:
            pos = self.open_pos.popleft()
            pos.update_tick()
            if pos.status == StatusOrder.closed:
                self.cl_pos[pos.id_order].append(pos)
            else:
                open_pos_.append(pos)

        self.open_pos = open_pos_

    def send_order(self, side: str, size: float,
                   tp: float = None, sl: float = None):
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

            if size ==0 or pos.side == side:
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
        

    def liquidate(self):
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
            self.send_order(side, size)

    def get_infos(self):
        """
        Provide information about all the different 
        orders (opened or closed).
        """
        info_open = self._trads_info_open()
        info_close = self._trads_info_close()

        infos = {
            "open_orders":vars(info_open),
            "closed_orders": info_close
            }
        
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
