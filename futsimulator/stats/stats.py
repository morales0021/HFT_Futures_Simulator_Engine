from futsimulator.positions.position import SideOrder
import pdb


class statPos():
    """
    A position stat object
    """
    def __init__(self):
        # open profit and loss
        self.o_pnl = float(0.0)
        # total size summing for a current type of position
        self.total_size = 0
        # average buy/sell open price variables
        self.av_o_price = float(0.0)
        # close profit and loss
        self.cl_pnl = float(0.0)
        # average delta time
        self.delta_t = float(0.0)
        # total orders in the pipe
        self.total_orders = 0
        # average close price
        self.av_cl_price = float(0.0)
        # position side
        self.side = None
        # takeprofit 
        self.takeprofit = []
        # stoploss
        self.stoploss = []
        # opened price
        self.opened = []

class statsPositions():
    
    def __init__(self):
        pass

    @classmethod
    def o_summarize(cls, positions: list = None):
        """
        Computes a set of information for all the
        opened positions:
        - open profit and loss
        - total size (buy, sell, and together)
        - average open price (buy, sell and together)
        - the average delta time (buy, sell and together)
          i.e. how much time in average since they were opened
        """
        b_s = statPos()
        
        if not positions:
            return b_s
        
        for pos in positions:
            # Set side
            b_s.side = pos.side
            # open pnl
            b_s.o_pnl += pos.o_pnl
            # total positions opened
            # warning : not fractional size allowed
            b_s.total_size += pos.size
            # total opened orders
            b_s.total_orders += 1
            # add average open price for later computation
            b_s.av_o_price +=  pos.o_price*pos.size
            # add average delta time
            b_s.delta_t += pos.delta_t*pos.size

            b_s.opened.append({
                "id_order": pos.id_order,
                "open_price": pos.o_price,
                "size": pos.size
            })

            if pos.tp:
                b_s.takeprofit.append({
                    "id_order": pos.id_order,
                    "tp":pos.tp,
                    "size":pos.size})

            if pos.sl:
                b_s.stoploss.append({
                    "id_order": pos.id_order,
                    "sl":pos.sl,
                    "size":pos.size})
               
        # compute average delta time
        b_s.delta_t /= b_s.total_size if b_s.total_size else 1.0

        # compute average open price
        b_s.av_o_price /= b_s.total_size if b_s.total_size else 1.0

        return b_s

    @classmethod
    def c_summarize(cls, positions: list = None):
        """
        Computes a set of information for the
        closed positions. In particular we pass by o_summarize
        because it allows to compute the next properties that some
        of them are valids for a closed position:
        - open profit and loss (not valid because position is now closed)
        - total size of the closed position (valid, and done for buy, sell, and together)
        - average open price (valid, and done for buy, sell and together)
        - the average delta time (valid, and done for buy, sell and together)
          i.e. how much time in average those orders lived
          since they were opened
        - the total closed profit and loss ( valid, and done for buy, sell and together)
        """
        b_s = cls.o_summarize(positions)

        if not positions:
            return b_s

        for pos in positions:
            # Compute properties 
            b_s.side = pos.side
            # close pnl
            b_s.cl_pnl += pos.cl_pnl
             # add average open price for later computation
            b_s.av_cl_price +=  pos.cl_price*pos.size       

        # comput average open price
        b_s.av_cl_price /= b_s.total_size if b_s.total_size else 1.0

        return b_s
