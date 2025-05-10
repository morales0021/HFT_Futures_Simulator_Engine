import textwrap

class MarketSnapshot():

    def __init__(self, idx, symbol, bid_arr, ask_arr, time_arr, 
                 indicators_arr):
        """
        Generates a market snapshot using the arrays of the historical data and the idx provided
        of the current step.
        The more important attributes in the MarketSnapshot are:
        - bid: the bid price of the current step
        - ask: the ask price of the current step
        """
        assert(type(idx)==int)

        try:
            self.idx = idx
            self.bid_arr = bid_arr
            self.ask_arr = ask_arr
            self.time_arr = time_arr
            self.indicators_arr = indicators_arr
            self.symbol = symbol
            self.bid = bid_arr[idx]
            self.ask = ask_arr[idx]
            self.time = time_arr[idx]
            self.indicators = indicators_arr[idx]

        except Exception as e:
            msg = ("Exception raised in marketSnaphot, check if index is"
                   "not bigger than lenght of attributes : ".format(e))
            raise Exception(msg)

    def step(self):
        """
        Updates the index of the market snaphshot by one
        unit
        """
        self.idx +=1
        self.bid = self.bid_arr[self.idx]
        self.ask = self.ask_arr[self.idx]
        self.time = self.time_arr[self.idx]
        self.indicators = self.indicators_arr[self.idx]

    def price_data(self):
        """
        Returns a dictionary with bid and ask data
        """
        return {'bid':self.bid, 'ask':self.ask}

    def indicator_data(self):
        return {"indicators": self.indicators}

    def get_side_price(self, side:str):
        """
        For a specific side 'b' for buy
        or 's' for sell, the model provides the 
        market price that will be used to open that 
        order
        """
        if side == 'b':
            return self.ask
        elif side == 's':
            return self.bid

    def __str__(self):

        cls_info = f"""
        bid: {self.bid},
        ask: {self.ask},
        time: {self.time},
        indicators: {self.indicators},
        idx: {self.idx}
        """

        return textwrap.dedent(cls_info)