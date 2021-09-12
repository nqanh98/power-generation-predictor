import json
import csv
from modules.time_helper import parse_time, check_str_time_btw_in_path
from modules.s3_helper import get_list_sub_foder
import os.path
from decouple import config

PLANT_CSV_PATH = config('PLANT_CSV_PATH')

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

# get loaded json data , process and write to csv file
def read_json_data(client, prefix , list_date_btw, bucket):
    print(list_date_btw)
    paginator = client.get_paginator('list_objects_v2')
    pages = paginator.paginate(Bucket=bucket, Prefix=prefix)
    # get all json data from s3
    if list_date_btw == 1:
        for page in pages:
            for obj in page['Contents']:
                if obj['Key'].find('pcs_summary/') != -1:
                    path = obj['Key']
                    # get json file with path
                    result = client.get_object(Bucket=bucket, Key=path)
                    data = result["Body"].read()
                    json_data = json.loads(data)
                    #check step time in file
                    if check_step_json_data(json_data) != 5:
                        print(f'Format data of {prefix} dont exactly !')
                        print('Done !')
                        return
                    else:
                        # run with step 5
                        path_of_file_output = get_name_output(path, 5)[0]
                        path_of_folder_output = get_name_output(path, 5)[1]
                        write_data_to_file(path_of_file_output, path_of_folder_output, json_data, 5)
                        # run with step 10
                        path_of_file_output = get_name_output(path, 10)[0]
                        path_of_folder_output = get_name_output(path, 10)[1]
                        write_data_to_file(path_of_file_output, path_of_folder_output, json_data, 10)
                        # run with step 30
                        path_of_file_output = get_name_output(path, 30)[0]
                        path_of_folder_output = get_name_output(path, 30)[1]
                        write_data_to_file(path_of_file_output, path_of_folder_output, json_data, 30)
        print(f'DONE : {prefix}')
        return
    # get data json from days btw latest day to today
    elif len(list_date_btw) >=1:
        for page in pages:
            for obj in page['Contents']:
                if obj['Key'].find('pcs_summary/') != -1 and check_str_time_btw_in_path(obj['Key'], list_date_btw):
                    path = obj['Key']
                    # get file json data with path
                    result = client.get_object(Bucket=bucket, Key=path)
                    data = result["Body"].read()
                    json_data = json.loads(data)
                    if check_step_json_data(json_data) != 5:
                        print(f'Format data of {prefix} dont exactly !')
                        return
                    else:
                        # run with step 5
                        path_of_file_output = get_name_output(path, 5)[0]
                        path_of_folder_output = get_name_output(path, 5)[1]
                        write_data_to_file(path_of_file_output, path_of_folder_output, json_data, 5)
                        # run with step 10
                        path_of_file_output = get_name_output(path, 10)[0]
                        path_of_folder_output = get_name_output(path, 10)[1]
                        write_data_to_file(path_of_file_output, path_of_folder_output, json_data, 10)
                        # run with step 30
                        path_of_file_output = get_name_output(path, 30)[0]
                        path_of_folder_output = get_name_output(path, 30)[1]
                        write_data_to_file(path_of_file_output, path_of_folder_output, json_data, 30)
        print(f'DONE {prefix}')
        return

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

# read data follow area ['ayabe', 'bobetsu'....]
def read_data_follow_plant(client , bucket, list_date_btw):
    list_foders = get_list_sub_foder(client, bucket)
    for folder in list_foders:
        prefix = folder + 'pcs/'
        print(f'Read data form {prefix}')
        read_json_data(client, prefix, list_date_btw, bucket)
    print('Done All')
    return
