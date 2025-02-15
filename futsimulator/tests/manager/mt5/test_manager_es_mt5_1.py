from futsimulator.manager.manager import PositionManager
from futsimulator.market.mt5snapshots import MT5Snapshot
from futsimulator.positions.position import SideOrder
from futsimulator.interfaces.redisindex import IndexDateDay
from datetime import datetime
import pytz
import pprint

host = '192.168.1.48'
port = 6379

start_time = datetime(year=2024, month=11, day=1, hour = 4, minute = 1, tzinfo = pytz.utc)
end_time = datetime(year=2024, month=11, day=1, hour = 12, minute = 0, tzinfo = pytz.utc)

idx_date_day = IndexDateDay(
    prefix = 'EP', suffix = 'idx',
    host = host, port = port, decimal_time=1e3
    )


snapshot = MT5Snapshot(host, port, idx_date_day = idx_date_day, 
                        start_time = start_time, end_time = end_time)



max_size = 2
commission_cfg = {}

ps = PositionManager(snapshot, max_size, commission_cfg)

# Update for the first time
snapshot.update()
ps.update()
side = SideOrder.sell
size = 2
ps.send_market_order(side, size)

print("Total opened orders")
result = ps.get_infos()
pprint.pprint(result)
print("The current snapshot is:")
print(snapshot)
print('-----------------------------------------------------------------------')

print("Sending a set of new buy orders")
side = SideOrder.buy
size = 4
ps.send_market_order(side, size)
print("Total opened orders")
result = ps.get_infos()
pprint.pprint(result)
print(snapshot)


print(("----------------------------------------------------"))
print("Executing a single update in price")
snapshot.update()
ps.update()
print("Total opened orders")
result = ps.get_infos()
pprint.pprint(result)
print(snapshot)