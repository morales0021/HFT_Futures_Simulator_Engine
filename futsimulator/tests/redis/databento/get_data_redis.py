import redis
import pdb
from futsimulator.format.databento import TBBO
from futsimulator.interfaces.redislist import RedisList

host_redis = '192.168.1.48'
port_redis = 6379
list_name = 'UB_20240331'
# r = redis.Redis(host = host_redis, port = port_redis)

rl = RedisList(host_redis, port_redis, list_name)
data = rl.read()
snap = TBBO(data,1000000000)
print(snap.ask)
print(snap.bid)
print(snap.ts)
print(snap.datetime)