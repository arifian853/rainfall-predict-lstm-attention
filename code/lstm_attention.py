import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.layers import Dense, LSTM, Input
from keras.layers import Layer
from keras import backend as K
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error

# Attention Layer Definition
class AttentionLayer(Layer):
    def __init__(self, **kwargs):
        super(AttentionLayer, self).__init__(**kwargs)

    def build(self, input_shape):
        self.W = self.add_weight(name="att_weight", shape=(input_shape[-1], 1), initializer="normal")
        self.b = self.add_weight(name="att_bias", shape=(input_shape[1], 1), initializer="zeros")
        super(AttentionLayer, self).build(input_shape)

    def call(self, x):
        et = K.squeeze(K.tanh(K.dot(x, self.W) + self.b), axis=-1)
        at = K.softmax(et)
        at = K.expand_dims(at, axis=-1)
        output = x * at
        return K.sum(output, axis=1)

    def compute_output_shape(self, input_shape):
        return input_shape[0], input_shape[-1]

# Load the dataset
rainfall_data_url = "https://raw.githubusercontent.com/arifian853/dataset-raw/master/data_cleaning2019_2020.csv"
rainfall_dataframe = pd.read_csv(rainfall_data_url, usecols=[3], engine='python')

# Plot the original dataset
plt.figure(figsize=(8,4))
plt.plot(rainfall_dataframe, label='Original data 2019-2020')
plt.legend()
plt.show()

# Convert to Numpy Array and Normalize
rainfall_array = rainfall_dataframe.values.astype('float32')
scaler_toolbox = MinMaxScaler(feature_range=(0, 1))
normalized_rainfall_data = scaler_toolbox.fit_transform(rainfall_array)

# Divide into Training and Test Segments
partition_size = int(len(normalized_rainfall_data) * 0.67)
remainder_size = len(normalized_rainfall_data) - partition_size
train_partition, test_partition = normalized_rainfall_data[0:partition_size,:], normalized_rainfall_data[partition_size:len(normalized_rainfall_data),:]

# Function to organize data for LSTM
def organize_data(sequence_data, history_length=1):
    input_data, target_data = [], []
    for idx in range(len(sequence_data)-history_length-1):
        fragment = sequence_data[idx:(idx+history_length), 0]
        input_data.append(fragment)
        target_data.append(sequence_data[idx + history_length, 0])
    return np.array(input_data), np.array(target_data)

history_length = 1
train_input, train_target = organize_data(train_partition, history_length)
test_input, test_target = organize_data(test_partition, history_length)

train_input = np.reshape(train_input, (train_input.shape[0], 1, train_input.shape[1]))
test_input = np.reshape(test_input, (test_input.shape[0], 1, test_input.shape[1]))

# Define input layer
input_layer = Input(shape=(1, history_length))

# LSTM layer
lstm_layer = LSTM(4, return_sequences=True)(input_layer)

# Attention layer
attention_output = AttentionLayer()(lstm_layer)

# Output layer
output_layer = Dense(1)(attention_output)

# Define the model
model = Model(inputs=input_layer, outputs=output_layer)

# Compile the model
model.compile(optimizer='adam', loss='mean_squared_error')

# Train the model
model.fit(train_input, train_target, epochs=100, batch_size=1, verbose=2)

# Make predictions
train_forecast = model.predict(train_input)
test_forecast = model.predict(test_input)

# Inverse transform the forecasts
train_forecast = scaler_toolbox.inverse_transform(train_forecast)
test_forecast = scaler_toolbox.inverse_transform(test_forecast)

# Calculate RMSE
train_rmse = np.sqrt(mean_squared_error(scaler_toolbox.inverse_transform([train_target])[0], train_forecast[:,0]))
test_rmse = np.sqrt(mean_squared_error(scaler_toolbox.inverse_transform([test_target])[0], test_forecast[:,0]))
print('Training RMSE:', train_rmse)
print('Testing RMSE:', test_rmse)

# Visualizing Original Data and Forecasts
plt.figure(figsize=(8,4))
plt.plot(scaler_toolbox.inverse_transform(normalized_rainfall_data), label='Original Rainfall Data')
plt.plot([item for item in train_forecast], label='Training Forecast')
plt.plot([item+len(train_forecast) for item in range(len(test_forecast))], test_forecast, label='Testing Forecast')
plt.legend()
plt.show()
