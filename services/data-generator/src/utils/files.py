import json
import csv
from utils.times import parse_time, get_list_str_time_btw_two_dates
from utils.s3 import get_list_sub_foder
import os

PLANT_CSV_PATH = os.getenv('PLANT_CSV_PATH')

# check step time in json data
# output 5 or 10 or 15
def check_step_json_data(json_data):
    time1 = parse_time(json_data[0]['timestamp'])
    time2 = parse_time(json_data[1]['timestamp'])
    hour = time2.hour - time1.hour
    minute = time2.minute - time1.minute
    return hour*60 + minute

# return name output_file_from_path, name_folder_to_read
# input hobetsu/pcs/2021/02/03/pcs_detail/hobetsu_1900821680_pcs_detail.json
# output  tuple of (plant-csv-data/hobetsu/「PCSNumber」/[Time]/「PCSNumber」.csv, hobetsu/pcs)
def get_name_output(path, step_time):
    list_worlds = path.split('/')
    last_world = list_worlds[-1]
    pcs_name = (last_world.split(list_worlds[0])[1]).split('_')[1]
    # print(pcs_name)
    file_name_output =  PLANT_CSV_PATH + list_worlds[0] + '/' + pcs_name + '/'+ str(step_time) + '/' + pcs_name + '.csv'
    folder_name_output = PLANT_CSV_PATH + list_worlds[0] + '/' + pcs_name + '/'+ str(step_time)
    return (file_name_output, folder_name_output)

# process data follow step time (5, 10, 15 and write to csv
def process_json_data(csv_writer, json_data, step):
    step_time_of_json_data = check_step_json_data(json_data)
    # step = 5,10,30 / 5 munites
    step = int(step/step_time_of_json_data)
    for i in range(0, len(json_data), step):
        if i + step < len(json_data):
            power = 0
            solar = 0
            for j in range(i, i+step):
                if 'env_sol' in json_data[j].keys() and 'kw' in json_data[j].keys():
                    solar += json_data[j]['env_sol']
                    power += json_data[j]['kw']
            time = parse_time(json_data[i]['timestamp'])
            month = time.month
            day = time.day
            hour = time.hour
            min = time.minute
            value = [time, power, solar, month, day, hour, min]
            csv_writer.writerow(value)
    return 0

# write to csv file
def write_data_to_file(path_of_file_output, path_of_folder_output, json_data, step_time):
    # if file is exists continue writing the content
    # else writing header first
    if os.path.exists(path_of_file_output):
        data_file = open(path_of_file_output, 'a')
        csv_writer = csv.writer(data_file)
        process_json_data(csv_writer, json_data, step_time)
        data_file.close()
    else:
        os.makedirs(path_of_folder_output)
        data_file = open(path_of_file_output, 'a')
        # create the csv writer object
        csv_writer = csv.writer(data_file)
        # writing headers to the CSV file
        header = ['timestamp', 'power', 'solar', 'month', 'day', 'hour', 'min']
        csv_writer.writerow(header)
        process_json_data(csv_writer, json_data, step_time)
        data_file.close()


# process json and write follow step (5 minutes, 10 minutes, 30 minutes....)
def create_file_output_and_write(path, json_data, step):
    path_of_file_output = get_name_output(path, step)[0]
    path_of_folder_output = get_name_output(path, step)[1]
    write_data_to_file(path_of_file_output, path_of_folder_output, json_data, step)


# get loaded json data , process and write to csv file
def read_json_data(client, bucket , list_date_btw):
    # read all json data from s3
    if list_date_btw ==1:
        for area in get_list_sub_foder(client, bucket):
            area = area + 'pcs/'
            print(area)
            try:
                for year in get_list_sub_foder(client, bucket, area):
                    for month in get_list_sub_foder(client, bucket, year):
                        for day in get_list_sub_foder(client, bucket, month):
                            day = day + 'pcs_summary/'
                            response = client.list_objects(Bucket=bucket, Prefix=day)
                            for content in response['Contents']:
                                # read json data and write
                                print(content['Key'])
                                result = client.get_object(Bucket=bucket, Key=content['Key'])
                                data = result["Body"].read()
                                json_data = json.loads(data)
                                if check_step_json_data(json_data) != 5:
                                    print(f'Format structure data of {area} wrong ! Not 5 minutes ')
                                    break
                                else:
                                    # create folder 5 minutes and write
                                    create_file_output_and_write(content['Key'], json_data, 5)
                                    # create folder 10 minutes and write
                                    create_file_output_and_write(content['Key'], json_data, 10)
                                    # create folder 30 minutes and write
                                    create_file_output_and_write(content['Key'], json_data, 30)
                                    continue
                print(f'Done {area}')
            except:
                continue
        print('Done all')
        return 0
    elif len(list_date_btw) >=1:
        for area in get_list_sub_foder(client, bucket):
            area = area + 'pcs/'
            print(area)
            for str_date in list_date_btw:
                sub_folder = area + str_date + 'pcs_summary/'
                response = client.list_objects(Bucket=bucket, Prefix=sub_folder)
                # check object exits with prefix
                if 'Contents' in response.keys():
                    for content in response['Contents']:
                        # read json data and write
                        print(content['Key'])
                        result = client.get_object(Bucket=bucket, Key=content['Key'])
                        data = result["Body"].read()
                        json_data = json.loads(data)
                        if check_step_json_data(json_data) != 5:
                            print(f'Format structure data of {area} wrong ! Not 5 minutes ')
                            break
                        else:
                            # create folder 5 minutes and write
                            create_file_output_and_write(content['Key'], json_data, 5)
                            # create folder 10 minutes and write
                            create_file_output_and_write(content['Key'], json_data, 10)
                            # create folder 30 minutes and write
                            create_file_output_and_write(content['Key'], json_data, 30)
                else:
                    continue
            print(f'Done {area}')
        print('Done all')
        return 0


