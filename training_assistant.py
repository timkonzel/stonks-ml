from stock_service import get_candle_data
import datetime
import math

def format_training_data(symbol):
    candle_data = get_candle_data(symbol)
    size = len(candle_data);
    training_input = [None] * size;
    training_output = [None] * size;
    for i in range(size):
        input_candle = candle_data[i]
        training_input[i] = i
        training_output[i] = input_candle['close']
    return { 'input': training_input, 'output': training_output }

def get_symbol_id(symbol):
    return int.from_bytes(symbol.encode(), 'little')
