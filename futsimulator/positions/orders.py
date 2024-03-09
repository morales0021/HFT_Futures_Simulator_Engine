class LimitStopOrder:

    def __init__(self, price, side, size, tp, sl):

        self.price = price
        self.size = size
        self.side = side
        self.tp = tp
        self.sl = sl