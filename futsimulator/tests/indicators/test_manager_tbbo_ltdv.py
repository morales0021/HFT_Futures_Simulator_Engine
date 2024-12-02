from futsimulator.market.redissnapshots import TBBOSnapshot
from futsimulator.indicators.profile import VolumeProfile
from futsimulator.indicators.traded_vol import TradedVolume
from enum import Enum
import pdb

"""
LAST TRADED VOLUME INDICATOR
This test is to check the TBBOSnapshot class
when including the TradedVolume class (indicator).

The TradedVolume class is a class that calculates the traded volume
for the bid and ask side of the order book.

The TradedVolume class has the following attributes:
- size_up: the size of the upper limit of the volume profile
- size_down: the size of the lower limit of the volume profile
- tick_unit: the tick unit of the traded volume
- type: the type of the traded volume (A for bid, B for ask)
- seconds: the time window for the traded volume calculation

The traded volume is calculated by the update method of the TradedVolume.
When the TBBOSnapshot is updated, the TradedVolume is also updated.
"""

# class TypeOffer(Enum):
#     bid = 1
#     ask = 2


host = '192.168.1.48'
port = 6379
list = 'UB_20240331'
decimal = 1e9
bid_sold = TradedVolume(size_up = 10, size_down=10,
                       tick_unit = 1/32, type = 'A', seconds = 10)
ask_bought = TradedVolume(size_up = 10, size_down=10,
                       tick_unit = 1/32, type = 'B', seconds = 10)

indicators = {
    'bid_sold': bid_sold,
    'ask_bought': ask_bought
    }
snapshot = TBBOSnapshot(host, port, list, decimal, indicators)
print("Printing snapshot")
print(snapshot)
print('End of printing snapshot\n\n')


for k in range(500):
    snapshot.update()

print("Printing Traded Volume for bid_sold and ask_bought")
print(snapshot.indicators['bid_sold'])
print(snapshot.indicators['ask_bought'])

print("Accessing the traded volume data")
print(snapshot.indicators['bid_sold'].ladder.data)