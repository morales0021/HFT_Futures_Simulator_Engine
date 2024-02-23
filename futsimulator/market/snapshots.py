class marketSnapshot():

    def __init__(self, idx, symbol, bid, ask, time, 
                 indicators, **kwargs):
        """
        Generates a market snapshot using the arrays
        of the historical data and the idx provided
        of the current step.
        """

        assert(type(idx)==int)

        try:
            self.symbol = symbol
            self.bid = bid[idx]
            self.ask = ask[idx]
            self.time = time[idx]
            self.indicators = indicators[idx]
        except Exception as e:
            msg = ("Exception raised in marketSnaphot, check if index is"
                   "not bigger than lenght of attributes : ".format(e))
            raise Exception(msg)

    def price_data(self):
        """
        Returns a dictionary with bid and ask data
        """
        return {'bid':self.bid, 'ask':self.ask}

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
