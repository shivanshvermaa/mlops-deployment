import pickle
import re
import os
import pandas as pd
import boto3
import shap

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
booster = loaded_model.get_booster()
explainer = shap.Explainer(booster)


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


def get_feature_importance():
    booster = loaded_model.get_booster()
    feature_importance = booster.get_score(importance_type='gain')
    return feature_importance

def get_batch_predictions(batch_df : pd.DataFrame):

    predictions = []

    for index, row in batch_df.iterrows():
        prediction = get_model_prediction(
            distance_from_home=row['distance_from_home'],
            distance_from_last_transaction=row['distance_from_last_transaction'],
            ratio_to_median_purchase_price=row['ratio_to_median_purchase_price'],
            repeat_retailer=row['repeat_retailer'],
            used_chip=row['used_chip'],
            used_pin_number=row['used_pin_number'],
            online_order=row['online_order']
        )
        predictions.append(prediction)

    return predictions
    
def get_prediction_and_explanation(distance_from_home:float=0,
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

    prediction = get_model_prediction(distance_from_home,
                        distance_from_last_transaction,
                        ratio_to_median_purchase_price,
                        repeat_retailer,
                        used_chip,
                        used_pin_number,
                        online_order)
    
    sample_df = pd.DataFrame(x_values_dictionary)

    shap_values = explainer(sample_df)

    # Return explanation as a dictionary
    explanation = {
        "shapValues": shap_values.values.tolist(),  # Convert SHAP values to a list
        "baseValue": shap_values.base_values.tolist(),  # Base value for the SHAP explanation
        "featureNames": sample_df.columns.tolist()  # Feature names used in the explanation
    }

    return explanation, prediction