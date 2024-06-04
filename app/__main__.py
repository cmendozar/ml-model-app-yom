from flask import Flask, request, jsonify
import pickle
import numpy as np

app = Flask(__name__)

with open('model.pkl', 'rb') as model_file:
    model = pickle.load(model_file)


@app.route('/')
def home():
    return '<h1>Server up</h1>'


@app.route('/predict-song', methods=['POST'])
def predict_song():
    data = request.json
    input_data = np.array([data['features']])
    prediction = model.predict(input_data)
    return jsonify({'prediction': prediction.tolist()})


@app.route('/predict-songs', methods=['POST'])
def predict_songs():
    return "<h1> Hola modelo </h1>"


if __name__ == '__main__':
    app.run(debug=True, port='8010')
