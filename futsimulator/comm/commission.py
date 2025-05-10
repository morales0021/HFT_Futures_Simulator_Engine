import pdb

class commission():
    """
    Defines the intelligence for computing the
    commission inside a position.
    """

    def __init__(self, config: dict = {}) -> None:

        self.config = config
        if config == {}:
            return
        
        self.type = config['type']
        
        assert(self.type in ['fixed','percent','mixed'])
        
        if self.type == 'fixed':
            self.value = config['value']
            assert(type(self.value) in [int, float])
        elif self.type == 'percent':
            self.percent = config['percent']
            assert(type(self.percent) in [int, float])
        else:
            self.percent = config['percent']
            self.value = config['value']
            assert(type(self.value) in [int, float])
            assert(type(self.percent) in [int, float])

    def get_com(self, pnl: float, price: float) -> float:
        """
        Computes the commission based on the precised configuration
        and returns the pnl after update w.r.t commission.
        """
        if self.config == {}:
            return pnl
        elif self.type == 'fixed':
            pnl -= self.value
            return pnl
        elif self.type == 'percent':
            pnl -=  price*self.percent
            return pnl
        elif self.type == 'mixed':
            pnl -= (price*self.percent + self.value)
        else:
            raise Exception("Unknown commission type")
