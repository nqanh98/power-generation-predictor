from utils.s3 import connect_s3, upload_data_to_s3
from utils.times import get_latest_date, get_list_str_time_btw_two_dates
from utils.files import  read_json_data
from datetime import datetime
from pathlib import Path
import pytz
import os

ACCESS_KEY = os.getenv('ACCESS_KEY')
SECRET_KEY = os.getenv('SECRET_KEY')
JSON_BUCKET = os.getenv('JSON_BUCKET')
CSV_BUCKET = os.getenv('CSV_BUCKET')
PLANT_CSV_PATH = os.getenv('PLANT_CSV_PATH')
TIMEZONE = os.getenv('TIMEZONE')

def process_with_date_plant(path = PLANT_CSV_PATH, bucket = JSON_BUCKET):
    if Path(path).is_dir():
        print('Run process json data from s3 latest day to today')
        latest_day = get_latest_date(path)
        today = datetime.now(pytz.timezone(TIMEZONE)).date()
        list_date_btw = get_list_str_time_btw_two_dates(latest_day, today)
        read_json_data(client, bucket, list_date_btw)
        # run process data json in s3 and upload new csv data with date
    else:
        # get all json date form s3
        print('Run process all json data from s3')
        list_date_btw = 1
        read_json_data(client, bucket, list_date_btw)
    return

if __name__ == '__main__':
    print('Start ....')
    start =  datetime.now()
    # connect s3
    client = connect_s3(ACCESS_KEY,SECRET_KEY)
    # read data json from s3, write to plant-csv-data
    process_with_date_plant(PLANT_CSV_PATH, JSON_BUCKET)
    # upload plant-csv-data to S3
    # upload_data_to_s3(client, CSV_BUCKET, PLANT_CSV_PATH)
    print('End: ', datetime.now())
    end = datetime.now()

    print('Time run: ', (end - start))

