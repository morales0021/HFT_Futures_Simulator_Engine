import pytz
from datetime import datetime
import pdb
from futsimulator.market.redissnapshots import TBBOSnapshot
from futsimulator.interfaces.redisindex import IndexDateDay

# info_dat = (
#     datetime(year=2024, month=4, day=2, hour = 4, minute = 1, tzinfo = pytz.utc),
#     datetime(year=2024, month=4, day=2, hour = 12, minute = 0, tzinfo = pytz.utc),
#     datetime(year=2024, month=4, day=2, hour = 12, minute = 30, tzinfo = pytz.utc)
#     )

info_dat = (
    datetime(year=2024, month=11, day=1, hour = 4, minute = 1, tzinfo = pytz.utc),
    datetime(year=2024, month=11, day=1, hour = 12, minute = 0, tzinfo = pytz.utc),
    datetime(year=2024, month=11, day=1, hour = 12, minute=30, tzinfo = pytz.utc)
    )


start_time_preload, start_time, end_time = info_dat
redis_host = '192.168.1.48'
redis_port = 6379

idx_date_day = IndexDateDay(
    prefix = 'EP', suffix = 'test_idx',
    host = redis_host, port = redis_port, decimal_time=1e3
    )

idx_s, idx_e, _,_ = idx_date_day.get_indexes(
    start_time=start_time_preload, end_time=start_time)

diff_pre = idx_e - idx_s
print("delta in preload ", diff_pre)

idx_s, idx_e, _,_ = idx_date_day.get_indexes(
    start_time=start_time, end_time=end_time)


print("index start ", idx_s)
print("index end ", idx_e)

diff_pre = idx_e - idx_s
print("delta after preload ", diff_pre)

