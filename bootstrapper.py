from training_assistant import format_training_data, get_most_recent_input_data
import tensorflow as tf
from tensorflow import keras
import numpy as np
import datetime

model = tf.keras.Sequential([
    keras.layers.Flatten(input_shape=[6]),
    keras.layers.Dense(128, activation=tf.nn.relu),
    keras.layers.Dense(10, activation=tf.nn.softmax)
])

model.compile(
    optimizer=tf.keras.optimizers.Adam(),
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

symbols = ['AMZN', 'TSLA', 'AAPL', 'MSFT', 'DAL', 'IZEA', 'GOOGL', 'FB', 'PG', 'NFLX', 'DIS', 'NVDA', 'KO', 'PEP']
all_input_data = []
all_output_data = []

for symbol in symbols:
    training_data = format_training_data(symbol)
    all_input_data += training_data['input']
    all_output_data += training_data['output']

training_input = np.array(all_input_data, dtype=float)
training_output = np.array(all_output_data, dtype=float)
model.fit(all_input_data, all_output_data, epochs=100)

for symbol in symbols:
    current_input = get_most_recent_input_data(symbol)
    time_value = datetime.datetime.fromtimestamp(current_input[1]).strftime('%Y-%m-%d %H:%M:%S')
    current_input_string = '[ Time: ' + time_value + ', Average Price: ' + str(round(current_input[2], 2)) + ', percent change: ' + str(round(current_input[3], 3)) + ', volume: ' + str(round(current_input[4], 2)) + ', recommendation: '+ str(round(current_input[5], 2)) + ' ]'
    print('Tomorrows prediction for ' + symbol + ' based on input: ' + current_input_string)
    print(model.predict([current_input])[0])
    print('\n')
