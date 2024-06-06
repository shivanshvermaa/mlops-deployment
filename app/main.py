import os
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
load_dotenv()

from model.model import get_model_prediction , __model_version__

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_KEY = os.getenv('AWS_SECRET_KEY')
AWS_S3_BUCKET_NAME = os.getenv('AWS_S3_BUCKET_NAME')
AWS_S3_OBJECT_NAME = os.getenv('AWS_S3_OBJECT_NAME')


app = FastAPI()

class TransactionIn(BaseModel):
    distance_from_home:float
    distance_from_last_transaction:float
    ratio_to_median_purchase_price:float
    repeat_retailer:int
    used_chip:int
    used_pin_number:int
    online_order:int

class PredictionOut(BaseModel):
    isFraudulent: bool


@app.get("/")
def home():
    return {"health_check": "OK", "model_version": __model_version__}

@app.post("/isFraudulent",response_model = PredictionOut)
def predict(payload : TransactionIn):
    model_prediction = get_model_prediction(distance_from_home=payload.distance_from_home,
                        distance_from_last_transaction=payload.distance_from_last_transaction,
                        ratio_to_median_purchase_price=payload.ratio_to_median_purchase_price,
                        repeat_retailer=payload.repeat_retailer,
                        used_chip=payload.used_chip,
                        used_pin_number=payload.used_pin_number,
                        online_order=payload.online_order)

    return {"isFraudulent" : model_prediction}