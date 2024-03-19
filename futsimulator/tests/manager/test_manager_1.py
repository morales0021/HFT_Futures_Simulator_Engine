from futsimulator.manager.manager import PositionManager
from futsimulator.market.snapshots import MarketSnapshot
from futsimulator.positions.position import SideOrder
import time
import pdb
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

ps = PositionManager(snapshot, max_b_size, max_s_size, commission_cfg)
side = SideOrder.buy
size = 5
tp = 45
sl = 7
ps.send_market_order(side, size, tp, sl)
assert(len(ps.open_pos) == 1)

size = 5
ps.send_market_order(side, size, tp, sl)
assert(len(ps.open_pos)==2)
print("Total opened orders")
result = ps.get_infos()
pprint.pprint(result)

print("Total after liquidation")
ps.liquidate()
result = ps.get_infos()
pprint.pprint(result)
assert(result['closed_orders'][1]['total_orders'] == 1)
assert(result['closed_orders'][2]['total_orders'] == 1)
assert(result['closed_orders'][1]['total_size'] == 5)
assert(result['closed_orders'][2]['total_size'] == 5)


# --------------------------------------------------
print("Second test")
side = SideOrder.buy
size = 5
tp = 45
sl = 7
ps.send_market_order(side, size, tp, sl)
assert(len(ps.open_pos) == 1)

snapshot.update()

size = 5
ps.send_market_order(side, size, tp, sl)
assert(len(ps.open_pos)==2)
print("Total opened orders")
result = ps.get_infos()
pprint.pprint(result)

snapshot.update()
print("Total after liquidation")
ps.liquidate()
result = ps.get_infos()
pprint.pprint(result)


for pos in ps.cl_pos:
    print(pos)