import os
import uvicorn
import time
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
load_dotenv()
import logging


from model.model import get_model_prediction , __model_version__ , get_feature_importance
from logging_setup import loggerSetup

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_KEY = os.getenv('AWS_SECRET_KEY')
AWS_S3_BUCKET_NAME = os.getenv('AWS_S3_BUCKET_NAME')
AWS_S3_OBJECT_NAME = os.getenv('AWS_S3_OBJECT_NAME')


# app = FastAPI()

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

class FeatureImportance(BaseModel):
    featureImportance: dict

# LOGGING SETUP
logger_setup = loggerSetup()

# GETTING LOGS
log = logging.getLogger(__name__)

def init_app():

    app = FastAPI(
        title = "Fraud Detection Endpoint",
        description = "ML-Ops Summer 2024",
        version = "1.0.0"
    )

    @app.on_event("startup")
    async def startup():
        nowutc = time.strftime("%Y-%m-%d %H:%M:%SZ", time.gmtime())
        log.info(f"APP STARTED AT : {nowutc}")
        pass

    @app.on_event("shutdown")
    async def shutdown():
        nowutc = time.strftime("%Y-%m-%d %H:%M:%SZ", time.gmtime())
        log.info(f"APP SHUTDOWN AT : {nowutc}")
        pass

    @app.get("/")
    def home():
        nowutc = time.strftime("%Y-%m-%d %H:%M:%SZ", time.gmtime())
        log.info(f"HEALTH CHECKUP AT : {nowutc}")
        return {"health_check": "OK", "model_version": __model_version__}

    @app.post("/isFraudulent",response_model = PredictionOut)
    def predict(payload : TransactionIn):

        nowutc = time.strftime("%Y-%m-%d %H:%M:%SZ", time.gmtime())
        log.info(f"PREDICTION REQUEST RECIEVED AT : {nowutc}")

        log.info(f"Received payload: distance_from_home={payload.distance_from_home}, "
         f"distance_from_last_transaction={payload.distance_from_last_transaction}, "
         f"ratio_to_median_purchase_price={payload.ratio_to_median_purchase_price}, "
         f"repeat_retailer={payload.repeat_retailer}, "
         f"used_chip={payload.used_chip}, "
         f"used_pin_number={payload.used_pin_number}, "
         f"online_order={payload.online_order}")


        model_prediction = get_model_prediction(distance_from_home=payload.distance_from_home,
                            distance_from_last_transaction=payload.distance_from_last_transaction,
                            ratio_to_median_purchase_price=payload.ratio_to_median_purchase_price,
                            repeat_retailer=payload.repeat_retailer,
                            used_chip=payload.used_chip,
                            used_pin_number=payload.used_pin_number,
                            online_order=payload.online_order)

        nowresponse = time.strftime("%Y-%m-%d %H:%M:%SZ", time.gmtime())
        
        log.info(f"PREDICTION RESPONED AT : {nowresponse} WITH {model_prediction} FOR REQUEST RECIEVED AT : {nowutc}")

        return {"isFraudulent" : model_prediction}

    @app.get("/featureImportance",response_model = FeatureImportance)
    def feature_importance():

        nowutc = time.strftime("%Y-%m-%d %H:%M:%SZ", time.gmtime())
        log.info(f"Feature Importance Requested at: {nowutc} for the model {__model_version__}")
        featureImportance  = get_feature_importance()

        log.info(f"Feature Importance RESPONED AT : {nowutc} WITH {featureImportance} FOR REQUEST RECIEVED AT : {nowutc}")

        return {"featureImportance" : featureImportance}

    # from controllers import home

    # app.include_router(home.router)

    return app

app = init_app()

if __name__ == '__main__':
    uvicorn.run("main:app",host="localhost",port=80,reload=True)