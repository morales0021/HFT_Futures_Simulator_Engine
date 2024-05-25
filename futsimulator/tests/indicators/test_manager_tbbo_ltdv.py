from futsimulator.market.redissnapshots import TBBOSnapshot
from futsimulator.indicators.profile import VolumeProfile
from futsimulator.indicators.ladder import PriceLadder
from typing import Literal

from enum import Enum

class TypeOffer(Enum):
    bid = 1
    ask = 2


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
                self.tick_unit
                )
            self.ladder_time = PriceLadder(
                snapshot.price, self.size_up, self.size_down,
                self.tick_unit, 0
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

host = '192.168.1.48'
port = 6379
list = 'UB_20240331'
decimal = 1e9
bid_sold = TradedVolume(size_up = 10, size_down=10,
                       tick_unit = 1/32, type = 'A', seconds = 10)
indicators = {'bid_sold': bid_sold}
snapshot = TBBOSnapshot(host, port, list, decimal, indicators)
print(snapshot)
for k in range(500):
    snapshot.update()
print(snapshot.indicators['bid_sold'])