from futsimulator.market.redissnapshots import TBBOSnapshot
from futsimulator.positions.orders import LimitStopOrder
from futsimulator.positions.position import SideOrder

host_redis = '192.168.1.48'
port_redis = 6379
list_name = 'UB_20240331'
decimal  = 1e9
tb = TBBOSnapshot(host_redis, port_redis, list_name, decimal)

for k in range(0,590):
    tb.update()

limit_order = LimitStopOrder(price = tb.ask, side = SideOrder.sell, size = 1)

for k in range(0,500):
    print("\n")
    if limit_order.price < tb.ask:
        print('The order was rather executed by a bid price')
        break

    print(tb.exec_order_by_queue(limit_order))
    if tb.side == 'B' and limit_order.price == tb.ask and tb.price == tb.ask:
        print("The ask was hitted at the limit order price")
    print(limit_order.price, tb.ask, tb.side, tb.size, limit_order.queue, tb.ask_sz_0, tb.idx)
    tb.update()
