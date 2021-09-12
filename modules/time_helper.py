from datetime import datetime, date, timedelta
import os.path
import pytz
from decouple import config
TIMEZONE = config('TIMEZONE')

# check latest modified file
def get_latest_date(path):
    latest_date = datetime.fromtimestamp(os.path.getmtime(path), pytz.timezone(TIMEZONE)).date() - timedelta(days=3)
    return latest_date
#convert time
def parse_time(x):
    return datetime.strptime(x, '%Y-%m-%dT%H:%M:%S+09:00')

# get list str tim between 2 dates
def get_list_str_time_btw_two_dates(date1, date2):
    date_modified = date1
    list_str_date = []
    while date_modified<date2:
        date_modified += timedelta(days=1)
        time_str = date_modified.strftime("%Y") + '/' + date_modified.strftime("%m") + '/' + date_modified.strftime("%d")
        list_str_date.append(time_str)

    return list_str_date

# check date in path
# check 2021/12/11 in path 'hobetsu/pcs/2021/12/11/pcs_name/pcs_summary/....csv
def check_str_time_btw_in_path(path, list_str_date):
    for str_date in list_str_date:
        if path.find(str_date) !=-1:
            return True
    return False
