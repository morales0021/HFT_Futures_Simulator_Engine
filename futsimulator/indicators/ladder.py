class PriceLadder:

    def __init__(self, center_price, size_up, size_down,
                 tick_unit, init_val = None):

        self.data = {}
        self.init_val = init_val
        for k in range(size_up,0,-1):
            self.data[center_price + k*tick_unit] = self.init_val

        self.data[center_price] = self.init_val

        for k in range(0,size_down+1,1):
            self.data[center_price - k*tick_unit] = self.init_val

    def reset(self):
        """
        Resets the price ladder to its initial state.
        """

        for key, _ in self.data.items():
            self.data[key] = self.init_val