from futsimulator.indicators.ladder import PriceLadder
from typing import Literal

class CurrentPrice:

    def __init__(self, size_up, size_down, tick_unit):
        """
        Defines the position of bid and ask.
        This indicator only work with TBBOSnapshot or any other
        class that contains the same attributes:
        - snapshot.ask
        - snapshot.bid
        - snapshot.init_price
        
        The MarketSnapshot class is not compatible with this indicator
        because it does not contain the attribute:
        - snapshot.init_price        
        """

        self.size_up = size_up
        self.size_down = size_down
        self.tick_unit = tick_unit
        self.ladder = None
        self.ladder_time = None
        self.price = None

    def update(self, snapshot):

        if not self.ladder:

            self.ladder = PriceLadder(
                snapshot.init_price, self.size_up, self.size_down,
                self.tick_unit, init_val = 0
                )
        else:
            self.ladder.reset()

        self.ladder.data[snapshot.ask] = 2
        self.ladder.data[snapshot.bid] = 1

        self.price = self.ladder.data

    def __str__(self):
        
        data = ""
        for key, value in self.ladder.data.items():
            if value:
                data += f"{key}: {value} \n"

        return data