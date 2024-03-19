class LimitStopOrder:

    def __init__(self, price, side, size, tp=None, sl=None, id_counter = None):

        self.price = price
        self.size = size
        self.side = side
        self.tp = tp
        self.sl = sl
        self.id_counter = id_counter