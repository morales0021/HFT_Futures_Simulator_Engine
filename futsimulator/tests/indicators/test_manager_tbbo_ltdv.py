from futsimulator.market.redissnapshots import TBBOSnapshot
from futsimulator.indicators.profile import VolumeProfile
from futsimulator.indicators.traded_vol import TradedVolume
from enum import Enum
import pdb


class TypeOffer(Enum):
    bid = 1
    ask = 2


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
print(snapshot)
for k in range(500):
    snapshot.update()
print(snapshot.indicators['bid_sold'])
print(snapshot.indicators['ask_bought'])
pdb.set_trace()

print(snapshot.indicators['bid_sold'].ladder.data)