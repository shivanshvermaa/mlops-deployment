import pickle
import re
import os
import pandas as pd
import boto3

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_KEY = os.getenv('AWS_SECRET_KEY')
AWS_S3_BUCKET_NAME = os.getenv('AWS_S3_BUCKET_NAME')
AWS_S3_OBJECT_NAME = os.getenv('AWS_S3_OBJECT_NAME')


s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_KEY
)

__model_version__ = AWS_S3_OBJECT_NAME.split('/')[1]
model_name = AWS_S3_OBJECT_NAME.split('/')[2]

s3_client.download_file(AWS_S3_BUCKET_NAME, AWS_S3_OBJECT_NAME,model_name)

loaded_model = pickle.load(open(model_name, "rb"))

def get_model_prediction(distance_from_home:float=0,
                        distance_from_last_transaction:float=0,
                        ratio_to_median_purchase_price:float=0,
                        repeat_retailer:int=0,
                        used_chip:int=0,
                        used_pin_number:int=0,
                        online_order:int=0):

    x_values_dictionary = {
        'distance_from_home': [distance_from_home],
        'distance_from_last_transaction': [distance_from_last_transaction],
        'ratio_to_median_purchase_price': [ratio_to_median_purchase_price],
        'repeat_retailer': [repeat_retailer],
        'used_chip': [used_chip],
        'used_pin_number': [used_pin_number],
        'online_order': [online_order]
    }
    
    sample_df = pd.DataFrame(x_values_dictionary)
        
    return bool(loaded_model.predict(sample_df)[0])
