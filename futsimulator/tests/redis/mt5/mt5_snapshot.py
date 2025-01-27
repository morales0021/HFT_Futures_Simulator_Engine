import pdb
from futsimulator.market.mt5snapshots import MT5Snapshot

host_redis = '192.168.1.48'
port_redis = 6379
list_name = 'EP_20241101_test'
tb = MT5Snapshot(host_redis, port_redis, list_name, "EP")

print(tb.ask)
print(tb.bid)
print(tb.ts)
print(tb.datetime)

pdb.set_trace()

print("\n")
tb.update()
print(tb.ask)
print(tb.bid)
print(tb.ts)
print(tb.datetime)

print("\n")
print(tb.price_data())
print(tb.get_side_price('b'))

print(tb)