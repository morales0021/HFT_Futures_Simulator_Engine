from futsimulator.data_readers.mt5_redis import MT5RedisReader

path = '/home/mora/Documents/projects/dataseries/mt5/EP/'
files = [
    "EP_202411010000_202411012059.csv",
    "EP_202312150000_202312172359.csv",
    "EP_202307010043_202307292042.csv"

]

host_redis = '192.168.1.48'
port_redis = 6379

mt5_reader = MT5RedisReader(
    host_redis=host_redis,
    port_redis=port_redis,
    identifier='EP'
    )

mt5_reader.load_data(path, files)