from futsimulator.market.redissnapshots import TBBOSnapshot
from futsimulator.indicators.price import CurrentPrice
from enum import Enum
import pdb


class TypeOffer(Enum):
    bid = 1
    ask = 2


host = '192.168.1.48'
port = 6379
list = 'UB_20240331'
decimal = 1e9
current_price = CurrentPrice(size_up = 10, size_down=10,
                       tick_unit = 1/32)

indicators = {
    'current_price': current_price
    }
snapshot = TBBOSnapshot(host, port, list, decimal, indicators)
print(snapshot)
for k in range(500):
    snapshot.update()
print(snapshot.indicators['current_price'])
print(snapshot.indicators['current_price'].price)