from futsimulator.manager.manager import PositionManager
from futsimulator.market.redissnapshots import TBBOSnapshot
from futsimulator.positions.position import SideOrder
import pprint

host = '192.168.1.48'
port = 6379
list = 'UB_20240331'
decimal = 1e9
snapshot = TBBOSnapshot(host, port, list, decimal)

max_b_size = 100
max_s_size = 100
commission_cfg = {}

ps = PositionManager(snapshot, max_b_size, max_s_size, commission_cfg)

snapshot.update()
ps.update()

side = SideOrder.sell
size = 10
ps.send_market_order(side, size)
print("Total opened orders")
result = ps.get_infos()
pprint.pprint(result)
print(snapshot)

price = 128.71875
side = SideOrder.sell
ps.send_limit_order(price, side, size)
result = ps.get_infos()
pprint.pprint(result)
print('\n')
print(snapshot)

for k in range(50):
    snapshot.update()
    ps.update()

result = ps.get_infos()
pprint.pprint(result)
print('\n')
print(snapshot)

side = SideOrder.buy
size = 20
ps.send_market_order(side, size)

result = ps.get_infos()
pprint.pprint(result)
print('\n')
print(snapshot)