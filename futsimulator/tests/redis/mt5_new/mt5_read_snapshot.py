import pdb
from futsimulator.market.mt5snapshots import MT5Snapshot
from futsimulator.data_readers.mt5_redis import MT5RedisReader
from datetime import datetime, timezone
host_redis = '192.168.1.48'
port_redis = 6379

# path = '/home/mora/Documents/projects/dataseries/mt5/EP/'
# files = [
#     "EP_202411010000_202411012059.csv",
#     "EP_202312150000_202312172359.csv",
#     "EP_202307010043_202307292042.csv"

# ]

mt5_reader = MT5RedisReader(
    host_redis=host_redis,
    port_redis=port_redis,
    identifier='EP'
)

mt5_reader.load_data(
    path = '/home/mora/Documents/projects/dataseries/mt5/EP/',
    files = [
        "EP_202307010043_202307292042.csv",
        "EP_202411010000_202411012059.csv",
        "EP_202312150000_202312172359.csv",
    ]
)

tb = MT5Snapshot(
    host_redis,
    port_redis,
    symbol = "symbol",
    mt5_reader= mt5_reader,
    start_time = datetime(2024, 11, 1, 14, 0, tzinfo=timezone.utc),
    end_time = datetime(2024, 11, 1, 17, 0, tzinfo=timezone.utc)
    )


print(tb)

tb.step()

print(tb)