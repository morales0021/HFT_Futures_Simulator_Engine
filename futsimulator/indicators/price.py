from futsimulator.indicators.ladder import PriceLadder
from typing import Literal

class CurrentPrice:

    def __init__(self, size_up, size_down, tick_unit):
        """
        Defines a the position of bid and ask
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