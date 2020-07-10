from training_assistant import format_training_data, get_most_recent_input_data
import tensorflow as tf
from tensorflow import keras
import numpy as np

model = tf.keras.Sequential([
    keras.layers.Flatten(input_shape=[7]),
    keras.layers.Dense(128, activation=tf.nn.relu),
    keras.layers.Dense(8, activation=tf.nn.softmax)
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
model.fit(all_input_data, all_output_data, epochs=500)

for symbol in symbols:
    print('Tomorrows prediction for ' + symbol)
    current_input = get_most_recent_input_data(symbol)
    print(model.predict([current_input])[0])
    print('\n')
