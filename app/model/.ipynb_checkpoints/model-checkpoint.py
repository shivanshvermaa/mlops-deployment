import pickle
import re
import pandas as pd

file_name = "xgb_reg.pkl"

xgb_model_loaded = pickle.load(open(file_name, "rb"))

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
        
    return bool(xgb_model_loaded.predict(sample_df)[0])
