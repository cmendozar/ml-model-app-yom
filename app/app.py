import pickle

from flask import Flask, request, jsonify
from app.preprocessing import AppPreprocessing

app = Flask(__name__)


@app.route('/')
def home():
    return '<h1>Server up</h1>'


with open('model.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

preprocessor = AppPreprocessing(None, None, None)


@app.route('/predict-song', methods=['POST'])
def predict():
    try:
        X = preprocessor.transform_request_to_df(request)
        prediction = model.predict(X)
        return jsonify({'prediction': prediction.tolist()})
    except ValueError as e:
        return jsonify({'error': str(e)}), 400


@app.route('/predict-songs', methods=['POST'])
def predict_songs():
    # TODO: Make a method to process many data songs
    # Could be a use case with these particularity
    return jsonify({'prediction': {'Song1': '1.0', 'Song2': '0.0'}})
