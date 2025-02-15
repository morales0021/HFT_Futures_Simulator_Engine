import pytz
from datetime import datetime
import pdb
from futsimulator.market.redissnapshots import TBBOSnapshot
from futsimulator.interfaces.redisindex import IndexDateDay

# info_dat = (
#     datetime(year=2024, month=4, day=2, hour = 4, minute = 1, tzinfo = pytz.utc),
#     datetime(year=2024, month=4, day=2, hour = 12, minute = 0, tzinfo = pytz.utc),
#     datetime(year=2024, month=4, day=2, hour = 12, minute = 30, tzinfo = pytz.utc)
#     )


redis_host = '192.168.1.48'
redis_port = 6379
tick_decimal = 1e9

idx_date_day = IndexDateDay(
    prefix = 'UB', suffix = 'zadd',
    host = redis_host, port = redis_port
    )



def check_delta_prices(snapshot,  tick):

    max_price = None
    init_price = None
    min_price = None

    while not snapshot.finished:
        if not init_price:

            init_price = snapshot.bid
            max_price = snapshot.bid
            min_price = snapshot.bid

        else:

            if max_price < snapshot.bid:
                max_price = snapshot.bid

            if min_price > snapshot.bid:
                min_price = snapshot.bid

        snapshot.update()

    delta_up = (max_price - init_price)/(tick)
    delta_do = (init_price - min_price)/(tick)

    return delta_up, delta_do, max_price, min_price

# 12 utc is 8 am in new york 
# 16 utc is 12 am in new york 

days = [1] #range(1,30)
days_dic = {}
for day in days:
    try:
        #day = 11
        month = 4
        year = 2024

        info_dat = (
            datetime(year=year, month=month, day=day, hour = 3, minute = 0, tzinfo = pytz.utc),
            datetime(year=year, month=month, day=day, hour = 3, minute = 1, tzinfo = pytz.utc),
            datetime(year=year, month=month, day=day, hour = 17, minute = 0, tzinfo = pytz.utc)
            )

        start_time_preload, start_time, end_time = info_dat

        snapshot = TBBOSnapshot(
            redis_host, redis_port, decimal = tick_decimal,
            idx_date_day = idx_date_day, start_time = start_time, end_time = end_time,
            start_time_preload = start_time_preload
            )

        tick = 1/32

        d_up, d_do, max_p, min_p = check_delta_prices(snapshot=snapshot, tick = tick)
        days_dic[day] = {"max_p": d_up, "min_p": d_do}
        print(days_dic)

    except Exception as e:
        print(e)
        continue

# print(d_up, d_do)
# print(max_p, min_p)