from futsimulator.manager.manager import PositionManager
from futsimulator.market.snapshots import MarketSnapshot
from futsimulator.positions.position import SideOrder
import pprint

def test_1():
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
    side = SideOrder.buy
    size = 5
    tp = 17
    sl = 5
    ps.send_market_order(side, size, tp, sl)

    price = 14
    side = SideOrder.buy
    size = 5
    tp = 19
    sl = 8
    ps.send_limit_order(price, side, size, tp, sl)
    ps.update()

    # Update tick to ask (12,13) and bid (11,12)
    for k in range(0,2):
        snapshot.update() # increment the tick index
        ps.update() # update the positions with the new tick

    result = ps.get_infos()
    pprint.pprint(result)

    print("\n")


#----------------------------
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
side = SideOrder.buy
size = 5
tp = 17
sl = 5
ps.send_market_order(side, size, tp, sl)

price = 14
side = SideOrder.buy
size = 5
tp = 19
sl = 8
ps.send_stop_order(price, side, size, tp, sl)
ps.update()

# Update tick to ask (12,13) and bid (11,12)
for k in range(0,5):
    snapshot.update() # increment the tick index
    ps.update() # update the positions with the new tick

result = ps.get_infos()
pprint.pprint(result)
print("\n")

ps.send_stop_order(price, side, size, tp, sl)
result = ps.get_infos()
pprint.pprint(result)

ps.send_limit_order(price, side, size, tp, sl)
result = ps.get_infos()
pprint.pprint(result)

ps.update()
result = ps.get_infos()
pprint.pprint(result)

ps.modify_ls_order(id_order = 5, tp = 50, sl = 1)
result = ps.get_infos()
pprint.pprint(result)

#----------------------------------------
ps.send_stop_order(price, side, size, tp, sl)
result = ps.get_infos()
pprint.pprint(result)


ps.modify_ls_order(id_order = 7, tp = 10, sl = 8)
result = ps.get_infos()
pprint.pprint(result)

ps.delete_ls_order(id_order=7)
ps.delete_ls_order(id_order=5)
result = ps.get_infos()
pprint.pprint(result)
