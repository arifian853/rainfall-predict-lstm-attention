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
data_url = "https://raw.githubusercontent.com/arifian853/dataset-raw/master/data_cleaning2019_2020.csv"
df = pd.read_csv(data_url)

# Filter data for 2021
df_2021 = df[df['Year'] == 2021]

# Select relevant columns
df_2021 = df_2021[['Tavg', 'RH_avg', 'RR', 'ddd_x', 'ff_avg']]

# Normalize the data
scaler = MinMaxScaler()
scaled_data = scaler.fit_transform(df_2021)

# Define function to organize data
def organize_data(sequence_data, history_length=1):
    input_data, target_data = [], []
    for idx in range(len(sequence_data)-history_length-1):
        fragment = sequence_data[idx:(idx+history_length), :]
        input_data.append(fragment)
        target_data.append(sequence_data[idx + history_length, 2])  # RR is at index 2
    return np.array(input_data), np.array(target_data)

# Organize data
history_length = 1
input_data, target_data = organize_data(scaled_data, history_length)

# Reshape input data
input_data = np.reshape(input_data, (input_data.shape[0], 1, input_data.shape[1]))

# Define input layer
input_layer = Input(shape=(1, input_data.shape[2]))

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
model.fit(input_data, target_data, epochs=100, batch_size=1, verbose=2)

# Make predictions
predictions = model.predict(input_data)

# Inverse transform the predictions
predicted_rr = scaler.inverse_transform(predictions)

# Visualize the predicted rainfall for 2021
plt.figure(figsize=(10, 6))
plt.plot(df_2021.index[1:], predicted_rr, label='Predicted RR for 2021', color='red')
plt.plot(df_2021.index[1:], df_2021['RR'].iloc[1:], label='Actual RR for 2021', color='blue')
plt.xlabel('Date')
plt.ylabel('Rainfall (mm)')
plt.title('Predicted vs Actual Rainfall (RR) for 2021')
plt.legend()
plt.grid(True)
plt.show()
