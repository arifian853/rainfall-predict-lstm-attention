from flask import Flask, request, jsonify
from flask_cors import CORS
import tensorflow as tf
import numpy as np
import joblib

app = Flask(__name__)
CORS(app)

# Load the SavedModels
model_lstm = tf.saved_model.load("saved_model_lstm")
model_lstm_attention = tf.saved_model.load("saved_model_lstm_attention")

# Load the scalers
scaler_X = joblib.load('./scaler/scaler_X.pkl')
scaler_y = joblib.load('./scaler/scaler_y.pkl')

# Print model summaries
print("Model information - LSTM: \t")
print(model_lstm.signatures)

print("Model information - LSTM with Attention: \t")
print(model_lstm_attention.signatures)

# Function to preprocess input data
def preprocess_input_data(data):
    features = ['Tavg', 'RH_avg', 'ss', 'ff_avg']
    X = np.array([[float(day[feature]) for feature in features] for day in data['input']])
    X = scaler_X.transform(X).reshape(-1, 10, 4).astype(np.float32)
    return X

def denormalize_output(predictions):
    return scaler_y.inverse_transform(predictions)

@app.route('/')
def home():
    return 'Hello World!'

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    print("Received JSON data:", data)

    # Preprocess input data
    X = preprocess_input_data(data)

    # Make predictions using the models
    predictions_lstm = model_lstm.signatures['serving_default'](lstm_14_input=tf.constant(X))['dense_4'].numpy()
    predictions_lstm_attention = model_lstm_attention.signatures['serving_default'](input_3=tf.constant(X))['dense_2'].numpy()

    # Denormalize predictions
    predictions_lstm_denorm = denormalize_output(predictions_lstm)
    predictions_lstm_attention_denorm = denormalize_output(predictions_lstm_attention)

    # Prepare the response
    response = {
        'predictions_lstm': predictions_lstm_denorm.tolist(),
        'predictions_lstm_attention': predictions_lstm_attention_denorm.tolist()
    }

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)