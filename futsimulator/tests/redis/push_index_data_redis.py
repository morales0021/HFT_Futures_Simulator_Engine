import redis
import pdb
import json

class InjectZadd:

    def __init__(self, host, port):

        self.r = redis.Redis(host = host, port = port)
        self.r.ping()
        
    def inject(self, lst_name, data):
        
        self.r.zadd(lst_name, data)

host_redis = '192.168.1.48'
port_redis = 6379
file = "/home/mora/Documents/projects/dataseries/databento/UB/glbx-mdp3-20240331.tbbo.json"
list_name_redis = 'UB_20240331_zadd'

r_inj = InjectZadd(host_redis, port_redis)

f = open(file)

for idx, info in enumerate(f.readlines()):
    info = json.loads(info)
    score = int(info['ts_recv'])
    data = {idx:score}
    r_inj.inject(list_name_redis,data)