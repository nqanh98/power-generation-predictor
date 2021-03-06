import boto3
import os
from botocore.client import Config


#connect aws s3
def connect_s3(ACCESS_KEY, SECRET_KEY):
    config = Config(connect_timeout=5, retries={'max_attempts': 0})
    print('Starting connect S3....')
    client = boto3.client('s3', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY, config=config)
    print('.................. done')
    return client

# return list sub folder
def get_list_sub_foder(client, bucket, sub_folder=''):
    list_foders = []
    result = client.list_objects(Bucket=bucket,Prefix=sub_folder, Delimiter='/')
    for sub_folder in result.get('CommonPrefixes'):
        list_foders.append(sub_folder.get('Prefix'))
    return list_foders

#upload all files in plant-csv-data
def upload_data_to_s3(s3, bucket, path):
    # get all files in plant-csv-data:
    for root, dirs, files in os.walk(path):
        for file in files:
            #  ........./plant-csv-data/nakashibetsu2/1901257513/30/1901257513.csv
            local_file_path = os.path.join(root, file)
            # /nakashibetsu2/1901257513/5/1901257513.csv
            upload_file_path = local_file_path.split(path)[1]
            s3.upload_file(local_file_path, bucket, upload_file_path)
    print('Upload to S3 done !')
    return 0








