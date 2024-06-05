from futsimulator.indicators.ladder import PriceLadder
from typing import Literal

class TradedVolume:

    def __init__(self, size_up, size_down, tick_unit,
                 type: Literal["A","B","N"], seconds = 10):
        """
        Defines a column of traded volume in the last 10 seconds
        interval
        """

        self.size_up = size_up
        self.size_down = size_down
        self.tick_unit = tick_unit
        self.seconds = seconds
        self.type = type
        self.ladder = None
        self.ladder_time = None
        self.volume = None

    def update(self, snapshot):

        if not self.ladder:

            self.ladder = PriceLadder(
                snapshot.price, self.size_up, self.size_down,
                self.tick_unit, init_val = 0
                )
            self.ladder_time = PriceLadder(
                snapshot.price, self.size_up, self.size_down,
                self.tick_unit, init_val = 0
                )
            
        if not self.type == snapshot.side:
            return

        if self.ladder.data[snapshot.price]:
            time_ = self.ladder_time.data[snapshot.price]
            if snapshot.time - time_ <= self.seconds:
                self.ladder.data[snapshot.price] += snapshot.size
            else:
                self.ladder.data[snapshot.price] = snapshot.size

            self.ladder_time.data[snapshot.price] = snapshot.time

        else:
            self.ladder.data[snapshot.price] = snapshot.size
            self.ladder_time.data[snapshot.price] = snapshot.time

        self.volume = self.ladder.data

    def __str__(self):
        
        data = ""
        for key, value in self.volume.items():
            if value:
                data += f"{key}: {value} \n"

        return data