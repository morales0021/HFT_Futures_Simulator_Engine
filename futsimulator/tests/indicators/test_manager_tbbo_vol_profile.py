from futsimulator.market.redissnapshots import TBBOSnapshot
from futsimulator.indicators.profile import VolumeProfile
import pdb
import numpy as np

host = '192.168.1.48'
port = 6379
list = 'UB_20240331'
decimal = 1e9


print("Printing snapshot")
profile = VolumeProfile(10,10,1/32)
indicators = {'profile': profile}
snapshot = TBBOSnapshot(host, port, list, decimal, indicators)
print(snapshot)
print('End of printing snapshot\n\n')

print("Printing Volume Profile")
for k in range(500):
    snapshot.update()
print(snapshot.indicators['profile'])
prf = snapshot.indicators['profile'].profile

print("Accessing the volume profile data")
val_dic = [val for key, val in prf.items()]
val = np.array(val_dic)
print(val.shape)