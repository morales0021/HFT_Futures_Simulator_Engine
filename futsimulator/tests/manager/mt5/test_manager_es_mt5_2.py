from futsimulator.manager.manager import PositionManager
from futsimulator.market.mt5snapshots import MT5Snapshot
from futsimulator.positions.position import SideOrder
from futsimulator.interfaces.redisindex import IndexDateDay
from datetime import datetime
import pytz
import pprint
import pdb

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

# print snapshot
print("The current snapshot is:")
print(snapshot)

# Sending a limit order for buy
size = 1
unit_tick = 0.25
price_sell = snapshot.ask + 5*unit_tick
price_buy = snapshot.bid - 5*unit_tick
ps.send_limit_order(price_sell, SideOrder.sell, size)
ps.send_limit_order(price_sell, SideOrder.sell, size)
ps.send_limit_order(price_buy, SideOrder.buy, size)

print("Total opened orders")

result = ps.get_infos()
pprint.pprint(result)
print("The current snapshot is:")
print(snapshot)
print('-----------------------------------------------------------------------')



snapshot.update()
ps.update()

ps.cancel_all()

pdb.set_trace()