from training_assistant import format_training_data
import tensorflow as tf
from tensorflow import keras
import numpy as np

model = tf.keras.Sequential([
    keras.layers.Dense(1, input_shape=[1])
])

model.compile(
    optimizer='adam',
    loss='mean_squared_error',
    metrics=['accuracy']
)

symbols = ['AMZN']
all_input_data = []
all_output_data = []

for symbol in symbols:
    training_data = format_training_data(symbol)
    all_input_data += training_data['input']
    all_output_data += training_data['output']

size = len(all_input_data)

training_input = np.array(all_input_data, dtype=float)
training_output = np.array(all_output_data, dtype=float)

model.fit(training_input, training_output, epochs=4000)

for symbol in symbols:
    print('\nPrediction for ' + symbol + ' ('+ str(all_output_data[size-1]) + ')')
    prediction = model.predict([size, size+9, size+29])
    print('\n1 day 10 day 30 day')
    print(prediction)
    print('\n')
