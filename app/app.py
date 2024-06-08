import atexit
import signal
import pickle
from flask import Flask, request, jsonify
from app.preprocessing import AppPreprocessing
from utils.mongo_handler import MongoHandler
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from model.monitoring import Monitoring
from apscheduler.triggers.cron import CronTrigger

app = Flask(__name__)


@app.route('/')
def home():
    return '<h1>Server up</h1>'


with open('model.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

preprocessor = AppPreprocessing(None, None, None)
mongo_handler = MongoHandler("URI_YOM_MONGO", "yom", "ml-app")


@app.route('/predict-song', methods=['POST'])
def predict():
    try:
        X = preprocessor.transform_request_to_df(request)
        prediction = model.predict(X)
        try:
            mongo_handler.save_request_data(request.get_json(), prediction)
        except:
            # TODO: MANAGE BETTER THESE CASES.
            print("Request has not been saved into MongoDB.")
        return jsonify({'prediction': prediction.tolist()})
    except ValueError as e:
        return jsonify({'error': str(e)}), 400


@app.route('/predict-songs', methods=['POST'])
def predict_songs():
    # TODO: Make a method to process many data songs
    # Could be a use case with these particularity
    return jsonify({'prediction': {'Song1': '1.0', 'Song2': '0.0'}})


scheduler = BackgroundScheduler()

monitoring_instance = Monitoring("URI_YOM_MONGO", "yom", "ml-app", "data/t1/")

@scheduler.scheduled_job(CronTrigger(hour=0, minute=0))
def scheduled_monitoring():
    monitoring_instance.run_monitoring()
    # TODO: ADD LOGIC TO DETECT WHEN PVALUE OF k2 is less than 0.05
    # SO WE CAN SEND AN ALERT WITH EMAIL (EASY TO DO)!
    # HERE THE DATA IS ALREADY SENDED TO NEPTUNE SO WE STILL CAN SEE DATA THERE


scheduler.start()

# STOP SCHEDULLER WHEN APP IS SHUTDOWN
atexit.register(lambda: scheduler.shutdown())
signal.signal(signal.SIGINT, lambda: scheduler.shutdown())

# port = int(os.environ.get("PORT", 8000))
# app.run(host='0.0.0.0', port=port)
