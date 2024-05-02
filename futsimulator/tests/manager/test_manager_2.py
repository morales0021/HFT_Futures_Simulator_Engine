from futsimulator.manager.manager import PositionManager
from futsimulator.market.snapshots import MarketSnapshot
from futsimulator.positions.position import SideOrder
import pprint

ask_arr = [11,12,13,14,15,16,17,18,19]
bid_arr = [10,11,12,13,14,15,16,17,18]
time_arr = [1,2,3,4,5,6,7,8,9,10]
indicators_arr = [1,2,3,4,5,6,7,8,9,10]
idx = 0
symbol = 'some'

snapshot = MarketSnapshot(
    idx, symbol, bid_arr, ask_arr, time_arr, indicators_arr
    )

max_b_size = 100
max_s_size = 100
commission_cfg = {}

# Open 5 buy orders at ask 11 and bid 10
ps = PositionManager(snapshot, max_b_size, max_s_size, commission_cfg)
side = SideOrder.buy
size = 5
tp = 45
sl = 7
ps.send_market_order(side, size, tp, sl)

# Update tick to ask 12 and bid 11
snapshot.update() # increment the tick index
ps.update() # update the positions with the new tick
result = ps.get_infos()
pprint.pprint(result)

# Open 5 buy orders at ask 12 and bid 11
size = 5
ps.send_market_order(side, size, tp, sl)

# Update tick to ask 13 and bid 12
snapshot.update()
ps.update()
result = ps.get_infos()
pprint.pprint(result)

## Close 7 orders (10 total opened)
## Close price is at ask 13 and bid 12
## --------------------------------------------------
print("\n")
for k in range(0,7):
    side = SideOrder.sell
    size = 1
    tp = 7
    sl = 45
    ps.send_market_order(side, size, tp, sl)

# Profit is
# (12-11)*5 + (12-12)*2 = 5
result = ps.get_infos()
pprint.pprint(result)
print('\n')

# Update tick to ask 14 and bid 13
snapshot.update()
ps.update()
# Close 3 buy orders and open 2 sell orders
for k in range(0,5):
    side = SideOrder.sell
    size = 1
    tp = 7
    sl = 45
    ps.send_market_order(side, size, tp, sl)

result = ps.get_infos()
pprint.pprint(result)
# Profit is
# (12-11)*5 + (12-12)*2 = 5
# (13-12)*3 = 3