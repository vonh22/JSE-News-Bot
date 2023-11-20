import datetime
import pytz

jamaica_timezone = pytz.timezone("America/Jamaica")

business_days = [0,1,2,3,4]

market_open = datetime.time(9, 30, 0)
market_close = datetime.time(13, 0, 0)

after_market_start = datetime.time(13, 1, 0)
after_market_end = datetime.time(19, 30, 0)

before_market_start = datetime.time(8, 0, 0)
before_market_end = datetime.time(9, 29, 0)



def calculate_time_out():
    current_time = datetime.datetime.now(jamaica_timezone).time()
    current_day = datetime.datetime.now(jamaica_timezone).weekday()
    if current_day in business_days:
        if before_market_start >= current_time <= before_market_end or after_market_start >= current_time <= after_market_end:
            return 120
        else:
            return 1800
    else:
        return 21600


