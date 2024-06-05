import redis
import pdb
from futsimulator.interfaces.redisinjectors import InjectStr2List

# class InjectStr2List:

#     def __init__(self, host, port):

#         self.r = redis.Redis(host = host, port = port)
#         self.r.ping()
        
#     def inject(self, lst_name, data):
        
#         self.r.rpush(lst_name, data)

host_redis = '192.168.1.48'
port_redis = 6379
file = "/home/mora/Documents/projects/dataseries/databento/UB/glbx-mdp3-20240331.tbbo.json"
list_name_redis = 'UB_20240331'

r_inj = InjectStr2List(host_redis, port_redis)

f = open(file)

for i in f.readlines():
    r_inj.inject(list_name_redis,i)