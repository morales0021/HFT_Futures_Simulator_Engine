from futsimulator.manager.manager import PositionManager
from futsimulator.market.snapshots import MarketSnapshot
from futsimulator.positions.position import SideOrder
import pprint

### Testing stop loss and opening multiple orders
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

# Open 5 sell orders at ask 11 and bid 10
ps = PositionManager(snapshot, max_b_size, max_s_size, commission_cfg)
side = SideOrder.sell
size = 5
tp = 7
sl = 14
ps.send_market_order(side, size, tp, sl)

# Update tick two times -> 11/12 -> 12/13
for k in range(0,2):
    snapshot.update() # increment the tick index
    ps.update() # update the positions with the new tick

result = ps.get_infos()
pprint.pprint(result)

print("\n")

# Sent order at ask 13 and bid 12
size = 2
tp = 9
sl = 16
ps.send_market_order(side, size, tp, sl)

# update tick to ask (14) and bid (13)
snapshot.update()
ps.update()

result = ps.get_infos()
pprint.pprint(result)
assert(result['closed_orders'][1]['cl_pnl'] == -20.0)
print("\n")

snapshot.update()
ps.update()

snapshot.update()
ps.update()

# ticket at ask (16) and bid (15)
result = ps.get_infos()
pprint.pprint(result)

assert(result['closed_orders'][2]['cl_pnl']==-8.0)