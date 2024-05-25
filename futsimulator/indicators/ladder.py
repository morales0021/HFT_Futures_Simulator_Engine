class PriceLadder:

    def __init__(self, center_price, size_up, size_down,
                 tick_unit, init_val = None):

        self.data = {}
        for k in range(size_up,0,-1):
            self.data[center_price + k*tick_unit] = init_val

        self.data[center_price] = init_val

        for k in range(0,size_down+1,1):
            self.data[center_price - k*tick_unit] = init_val