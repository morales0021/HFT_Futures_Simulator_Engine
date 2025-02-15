import pdb
import tqdm
from futsimulator.market.mt5snapshots import MT5Snapshot
from futsimulator.indicators.timeframes.second_tf import TimeFrame

host_redis = '192.168.1.48'
port_redis = 6379
list_name = 'EP_20241101_test'
indicators = {
    "timeframe": TimeFrame(1)
}
tb = MT5Snapshot(host_redis, port_redis, list_name, "EP", indicators=indicators)


for k in tqdm.tqdm(range(500000)):
    tb.update()
    # print(tb.datetime)
    # print(tb.indicators['timeframe'].aggregator.aggregated_data) 