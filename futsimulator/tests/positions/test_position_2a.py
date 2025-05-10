from futsimulator.positions.position import Position
from futsimulator.positions.position import StatusOrder, SideOrder
from futsimulator.market.snapshots import MarketSnapshot
import time

# Buy order with stop loss
otime = time.time()
side = SideOrder.buy
symbol = 'eurusd'
tp = 17
sl = 7
size = 3.0

ask_arr = [11,9,8,7,6,16,17,18,19]
bid_arr = [10,8,7,6,5,15,16,17,18]
time_arr = [1,2,3,4,5,6,7,8,9,10]
indicators_arr = [1,2,3,4,5,6,7,8,9,10]
idx = 0

snapshot = MarketSnapshot(
    idx, symbol, bid_arr, ask_arr, time_arr, indicators_arr
    )

# Create a new position with properties
# Entry price ask 11
pos = Position(snapshot, side, size, tp, sl)


for k in range(0,7):
    snapshot.update()
    pos.update_tick()

print(pos)
assert(pos.cl_pnl == (7-11)*3.0)