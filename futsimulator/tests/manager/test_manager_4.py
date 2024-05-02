from futsimulator.manager.manager import PositionManager
from futsimulator.market.snapshots import MarketSnapshot
from futsimulator.positions.position import SideOrder
import pprint, pdb

# def test_1():
#     ### Testing stop loss and opening multiple orders
#     ask_arr = [11,12,13,14,15,16,17,18,19]
#     bid_arr = [10,11,12,13,14,15,16,17,18]
#     time_arr = [1,2,3,4,5,6,7,8,9,10]
#     indicators_arr = [1,2,3,4,5,6,7,8,9,10]
#     idx = 0
#     symbol = 'some'

#     snapshot = MarketSnapshot(
#         idx, symbol, bid_arr, ask_arr, time_arr, indicators_arr
#         )

#     max_b_size = 100
#     max_s_size = 100
#     commission_cfg = {}

#     # Open 5 sell orders at ask 11 and bid 10
#     ps = PositionManager(snapshot, max_b_size, max_s_size, commission_cfg)
#     side = SideOrder.buy
#     size = 5
#     tp = 17
#     sl = 5
#     ps.send_market_order(side, size, tp, sl)

#     price = 14
#     side = SideOrder.buy
#     size = 5
#     tp = 19
#     sl = 8
#     ps.send_limit_order(price, side, size, tp, sl)
#     ps.update()

#     # Update tick to ask (12,13) and bid (11,12)
#     for k in range(0,2):
#         snapshot.update() # increment the tick index
#         ps.update() # update the positions with the new tick
#     result = ps.get_infos()
#     pprint.pprint(result)
#     print("\n")
#----------------------------

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
#ps.update()

for k in range(0,5):
    snapshot.update() # increment the tick index
    ps.update() # update the positions with the new tick

result = ps.get_infos()
pprint.pprint(result)
print("\n")
print(snapshot)
# -----------------------------------
# Second print
# Send stop order
# -----------------------------------
print("Send a buy stop order with price ", price)
print("""The stop order is automatically executed because the price is already lower
      than the current price""")
ps.send_stop_order(price, side, size, tp, sl)
result = ps.get_infos()
pprint.pprint(result)
print('\n')

# -----------------------------------
# Third print
# Send limit order
# -----------------------------------
print("Send a limit buy order with price ", price)
print("The limit order remains pending because price is lower than the current price")
ps.send_limit_order(price, side, size, tp, sl)
result = ps.get_infos()
pprint.pprint(result)
print('\n')

# -----------------------------------
# Fourth print
# Modify a limit or stop order
# -----------------------------------
# print("Only update manager")
# ps.update()
# result = ps.get_infos()
# pprint.pprint(result)
# print('\n')
tp = 50
sl = 1
print(f"Modify the limit order, its take profit {tp} and stop loss {sl}")
ps.modify_ls_order(id_order = 6, tp = tp, sl = sl)
result = ps.get_infos()
pprint.pprint(result)

print('\n')
#----------------------------------------
print(f"""Send a new stop order with price {price}, size {size}, take profit {tp} and {sl}."""
       """Such order is automatically executed""")
ps.send_stop_order(price, side, size, tp, sl)
result = ps.get_infos()
pprint.pprint(result)


print('\n')
print('Delete the limit order')
ps.delete_ls_order(id_order=6)
result = ps.get_infos()
pprint.pprint(result)
