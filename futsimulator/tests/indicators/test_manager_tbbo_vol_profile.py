from futsimulator.market.redissnapshots import TBBOSnapshot
from futsimulator.indicators.profile import VolumeProfile


host = '192.168.1.48'
port = 6379
list = 'UB_20240331'
decimal = 1e9
profile = VolumeProfile(10,10,1/32)
indicators = {'profile': profile}
snapshot = TBBOSnapshot(host, port, list, decimal, indicators)
print(snapshot)
for k in range(500):
    snapshot.update()
print(snapshot.indicators['profile'])