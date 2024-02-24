from futsimulator.positions.position import Position
from futsimulator.positions.position import StatusOrder, SideOrder
from futsimulator.market.snapshots import MarketSnapshot
import time

# Check take profit in sell order
otime = time.time()
side = SideOrder.sell
symbol = 'eurusd'
tp = 7
sl = 15
size = 3.0

ask_arr = [11,10,9,8,7,6,17,18,19]
bid_arr = [10,9,8,7,6,5,16,17,18]
time_arr = [1,2,3,4,5,6,7,8,9,10]
indicators_arr = [1,2,3,4,5,6,7,8,9,10]
idx = 0

snapshot = MarketSnapshot(
    idx, symbol, bid_arr, ask_arr, time_arr, indicators_arr
    )

# Create a new position with properties
# Entry price bid 10
pos = Position(snapshot, side, size, tp, sl)


for k in range(0,7):
    snapshot.update()
    pos.update_tick(snapshot)

print(pos)
assert(pos.cl_pnl == (10 - 7)* 3.0)