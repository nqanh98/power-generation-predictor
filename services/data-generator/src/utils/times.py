from datetime import datetime, date, timedelta
import os
import pytz

TIMEZONE = os.getenv('TIMEZONE')

# check latest modified file
def get_latest_date(path):
    # 2021-09-01T00:00:00+09:00
    latest_date = datetime.fromtimestamp(os.path.getmtime(path), pytz.timezone(TIMEZONE)).date()
    return latest_date
#convert time
def parse_time(x):
    if x.split('+')[1] == '0900':
        return datetime.strptime(x, '%Y-%m-%dT%H:%M:%S+0900')
    else:
        return datetime.strptime(x, '%Y-%m-%dT%H:%M:%S+09:00')

# get list str tim between 2 dates
def get_list_str_time_btw_two_dates(date1, date2):
    date_modified = date1
    list_str_date = []
    while date_modified<date2:
        date_modified += timedelta(days=1)
        time_str = date_modified.strftime("%Y") + '/' + date_modified.strftime("%m") + '/' + date_modified.strftime("%d") + '/'
        list_str_date.append(time_str)

    return list_str_date
