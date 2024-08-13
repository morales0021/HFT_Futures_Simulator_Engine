from futsimulator.manager.manager import PositionManager
from futsimulator.market.redissnapshots import TBBOSnapshot
from futsimulator.positions.position import SideOrder
from futsimulator.interfaces.redisindex import IndexDateDay
from futsimulator.indicators.positions import CurrentPositions

from datetime import datetime
import pytz
import pprint

host = '192.168.1.48'
port = 6379
decimal = 1e9

start_time = datetime(year=2024, month=3, day=31, hour = 22, minute = 0, tzinfo = pytz.utc)
end_time = datetime(year=2024, month=3, day=31, hour = 23, minute=1, tzinfo = pytz.utc)

idx_date_day = IndexDateDay(
    prefix = 'UB', suffix = 'zadd',
    host = host, port = port
    )

snapshot = TBBOSnapshot(host, port, decimal = decimal, idx_date_day= idx_date_day,
                        start_time = start_time, end_time = end_time )

max_b_size = 100
max_s_size = 100
commission_cfg = {}
positions = CurrentPositions(10,10,1/32)
indicators = {"positions": positions}
ps = PositionManager(snapshot, max_b_size, max_s_size, commission_cfg, indicators)

snapshot.update()
ps.update()

side = SideOrder.buy
size = 10
ps.send_market_order(side, size)
print("Total opened orders")
result = ps.get_infos()
pprint.pprint(result)
print(snapshot)

print(ps.indicators['positions'].positions)