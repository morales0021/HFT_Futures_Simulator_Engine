from futsimulator.manager.manager import PositionManager
from futsimulator.market.snapshots import MarketSnapshot
from futsimulator.positions.position import SideOrder
import pprint, pdb

# -----------------------------------
# First print
# Send market order
# Send stop order
# -----------------------------------
print("Send a market order and a stop order")
ask_arr = [11,12,13,14,15,16,17,18,19]
bid_arr = [10,11,12,13,14,15,16,17,18]
time_arr = [1,2,3,4,5,6,7,8,9,10]
indicators_arr = [1,2,3,4,5,6,7,8,9,10]
idx = 0
symbol = 'some'

snapshot = MarketSnapshot(
    idx, symbol, bid_arr, ask_arr, time_arr, indicators_arr
    )

max_size = 100
commission_cfg = {}

# Open 5 sell orders at ask 11 and bid 10
ps = PositionManager(snapshot, max_size, commission_cfg)
side = SideOrder.buy
size = 5
tp = 17
sl = 5
ps.send_market_order(side, size, tp, sl)

for k in range(0,5):
    snapshot.update() # increment the tick index
    ps.update() # update the positions with the new tick

result = ps.get_infos()
pprint.pprint(result)
print("\n")
print(snapshot)

id_order = 1
sl = 9
tp = 20
print(f"Modifying a market order with {tp} and {sl}")
ps.modify_market_order(id_order, tp, sl)
result = ps.get_infos()
pprint.pprint(result)
print("\n")


id_order = 1
sl = 9
tp = 12
print(f"Modifying a market order with {tp} and {sl} which is then automatically closed")
ps.modify_market_order(id_order, tp, sl)
result = ps.get_infos()
pprint.pprint(result)
print("\n")