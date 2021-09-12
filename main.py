from modules.s3_helper import connect_s3, upload_data_to_s3
from modules.time_helper import get_latest_date, get_list_str_time_btw_two_dates
from modules.file_helper import  read_data_follow_plant
from datetime import datetime
from pathlib import Path
import pytz
from decouple import config

ACCESS_KEY = config('ACCESS_KEY')
SECRET_KEY = config('SECRET_KEY')
JSON_BUCKET = config('JSON_BUCKET')
CSV_BUCKET = config('CSV_BUCKET')
PLANT_CSV_PATH = config('PLANT_CSV_PATH')
TIMEZONE = config('TIMEZONE')

def process_with_date_plant(path = PLANT_CSV_PATH, bucket = JSON_BUCKET):
    if Path(path).is_dir():
        print('Run process json data from s3 latest day to today')
        latest_day = get_latest_date(path)
        today = datetime.now(pytz.timezone(TIMEZONE)).date()
        list_date_btw = get_list_str_time_btw_two_dates(latest_day, today)
        read_data_follow_plant(client, bucket, list_date_btw)
        # run process data json in s3 and upload new csv data with date
    else:
        # get all json date form s3
        print('Run process all json data from s3')
        list_date_btw = 1
        read_data_follow_plant(client, bucket, list_date_btw)
    return




if __name__ == '__main__':
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

