from collections import defaultdict, deque
from envtrading.positions.position import position
from envtrading.positions.stats import statsPositions
from envtrading.environ.market.snapshots import marketSnapshot 
import pdb

OPP_ORDER = {'b':'s', 's':'b'}
OPP_POS = {'b':'s', 's':'b'}

class PositionManager():
   
    def __init__(self, **kwargs):
        
        self.kwargs_reset = kwargs
        self.open_pos = defaultdict(deque)
        self.cl_pos = defaultdict(deque)
        self.rec_pos = defaultdict(deque)
        self.max_b_size = kwargs.get('max_b_size',100)
        self.max_s_size = kwargs.get('max_s_size',100)
        self.com_cfg = kwargs.get('commission_cfg',{})

    def reset(self):
        """
        Resets the Position Manager to its initial
        state
        """
        self.__init__(**self.kwargs_reset)

    def _restrict_size(self, symbol, side, size):
        """
        Restricts the amount of size you can have opened in buy and
        sell positions per symbol. 
        The max size in buy is independent from the max size in sell
        positions.
        Note that positions are calculated as netted.
        If size to be opened is superieur to max allowed then
        side is transformed to None.
        """
        # This restreins the total size to handle in buy or sell side 
        b, s, b_s = self._trads_info(symbol, 'open')
        stat_obj = b if side == 'b' else s
        max_cond = self.max_b_size if side == 'b' else self.max_s_size
        if stat_obj.total_size + size > max_cond:
            side = None

        return side
  
    def send_order(self, ms: marketSnapshot, side: str, size: float, 
                   symbol: str, **kwargs):
        """
        Receive an order and will open or close a position
        based on the current state of the positions being handled.
        """
        # This restreins the total size to handle in buy or sell side 
        side = self._restrict_size(symbol, side, size)

        # Recreate rec_pos at every send order
        self.rec_pos[symbol] = deque()
        # When side is none, it means we do nothing
        if side == None or size == 0:
            return

        open_pos_ = deque()
        """
        recent position is cleaned everytime
        we receive a new set of orders
        """ 
        
        # Loop over all the current opened positions
        while self.open_pos.get(symbol):

            pos = self.open_pos[symbol].popleft()

            if size == 0 or pos.side == side:
                """
                Keep current open position still in
                the pipe of opened positions
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
                    
                    # Transform size orders to closed positions
                    #pos.cl_price = price
                    pos.cl_price = ms.get_side_price(side)
                    pos.cl_time = ms.time
                    pos.size = size # Closed quantity
                    pos.cl_profit() # Update closed profit
                    pos.o_pnl = 0 # open profit and loss is zero because position is closed
                    self.cl_pos[symbol].append(pos)
                    self.rec_pos[symbol].append(pos)
                    
                    if remain:
                        pos = position(pos.o_price, pos.o_time,
                                       pos.side, remain, symbol,
                                       commission_cfg = self.com_cfg.get(symbol,{})
                                       )
                        
                        open_pos_.append(pos)

                    #Update size to be zero
                    size = 0

                # If size of the order is more than current opened positions
                # then close that batch of positions, and recalculate the
                # remaining size of orders to process
                elif pos.size - size < 0 :
                    """
                    Set the total position that will be closed
                    and add it to the stack of recent closed.
                    """
                    pos.cl_price = ms.get_side_price(side)
                    pos.cl_time = ms.time
                    pos.cl_profit() # Update closed profit
                    pos.o_pnl = 0 # open profit and loss is zero because position is closed
                    self.cl_pos[symbol].append(pos)
                    self.rec_pos[symbol].append(pos)

                    """
                    Update size to be filled for next position to be 
                    analysed
                    """
                    size -= pos.size
        
        """
        Open a position with the remaining size
        """
        if size > 0:
            pos = position(ms.get_side_price(side), ms.time, side, size, symbol,
                           commission_cfg = self.com_cfg.get(symbol,{})
                           )
            # updates immediately the open profit when opening a position
            price_data = ms.price_data()
            pos.op_profit(price_data)
            open_pos_.append(pos)

        self.open_pos[symbol] = open_pos_
    
    def liquidate(self, symbol, ms: marketSnapshot):
        """
        Liquidates all the opened orders and returns the
        current closed profit and loss realised by such
        liquidatetion
        """
        cpnl = 0
        opp_orders = []
        for pos in self.open_pos.get(symbol):
            side = OPP_ORDER[pos.side] 
            size = pos.size
            opp_orders.append((side,size))
        
        for op_ord in opp_orders:
            side, size = op_ord
            self.send_order(ms, side, size, symbol)
            cpnl += self.recent_cpnl(symbol)

        return cpnl

    def tick_update(self, symbol, price_data, now_time):
        """
        Update the opened orders, for index, opnl, and 
        time
        """
        for pos in self.open_pos[symbol]:
            
            pos.index += 1
            pos.op_profit(price_data)
            pos.cl_time = now_time
            pos.delta_time()

    def cpnl(self, symbol):
        """
        Computes the total closed profit and loss since the
        beguinning of the episode.
        Managed by statPositions object.
        """
        _,_,b_s = self._trads_info(symbol, 'close')

        return b_s.cl_pnl

    def recent_cpnl(self, symbol):
        """
        Computes the closed profit and loss
        for any position that remain in the recent position.
        Managed by statPositions object.
        """
        _,_,b_s = self._trads_info(symbol, 'recent')

        return b_s.cl_pnl

    def opnl(self, symbol):
        """
        Computes the open profit and loss
        for any position that remain in the open position.
        Managed by statPositions object.
        """
        _, _, b_s = self._trads_info(symbol, 'open')

        return b_s.o_pnl

    def _trads_info(self, symbol, type_pos):
        """
        Summarizes the trades information for
        the open trades for an specific symbol:
        like the open profit and loss
        for any position that remain in the open position.
        """
        if type_pos == 'open':
            b,s, b_s = statsPositions.o_summarize(self.open_pos.get(symbol))
        elif type_pos == 'close':
            b,s, b_s = statsPositions.c_summarize(self.cl_pos.get(symbol))
        elif type_pos == 'recent':
            b,s, b_s = statsPositions.c_summarize(self.rec_pos.get(symbol))
        else:
            raise Exception("Unknown trade info type")

        return b, s, b_s
