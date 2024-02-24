from futsimulator.positions.position import Position
from futsimulator.positions.position import StatusOrder, SideOrder
from futsimulator.market.snapshots import MarketSnapshot
import time

otime = time.time()
side = SideOrder.buy
symbol = 'eurusd'
tp = 17
sl = 7
size = 3.0

ask_arr = [11,12,13,14,15,16,17,18,19]
bid_arr = [10,11,12,13,14,15,16,17,18]
time_arr = [1,2,3,4,5,6,7,8,9,10]
indicators_arr = [1,2,3,4,5,6,7,8,9,10]
idx = 0

snapshot = MarketSnapshot(
    idx, symbol, bid_arr, ask_arr, time_arr, indicators_arr
    )

# Create a new position with properties
# Entry price ask 11
pos = Position(snapshot, side, size, tp, sl)
print(pos.o_pnl)

# Price at ask 12
snapshot.update()
pos.update_tick(snapshot)
print(pos.o_pnl)

# Price at ask 13
snapshot.update()
pos.update_tick(snapshot)
print(pos.o_pnl)
print(size)
print(pos)
assert(pos.o_pnl == (12-11)*3.0)