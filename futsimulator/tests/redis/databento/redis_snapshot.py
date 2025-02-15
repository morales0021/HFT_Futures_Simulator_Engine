from futsimulator.market.redissnapshots import TBBOSnapshot

host_redis = '192.168.1.48'
port_redis = 6379
list_name = 'UB_20240331'
decimal  = 1e9
tb = TBBOSnapshot(host_redis, port_redis, list_name, decimal)

print(tb.ask)
print(tb.bid)
print(tb.ts)
print(tb.datetime)

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