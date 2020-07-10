from stock_service import get_candle_data
import math

def format_training_data(symbol):
    candle_data = get_candle_data(symbol)
    size = len(candle_data) - 1;
    training_input = [None] * size;
    training_output = [None] * size;
    for i in range(size):
        input_candle = candle_data[i]
        next_candle = candle_data[i+1]
        training_input[i] = get_input_for_candle(input_candle, symbol)
        average_input_candle_price = (input_candle['open'] + input_candle['close'] + input_candle['high'] + input_candle['low']) / 4
        average_next_candle_price = (next_candle['open'] + next_candle['close'] + next_candle['high'] + next_candle['low']) / 4
        average_price_change = average_next_candle_price - average_input_candle_price
        percent_change = (average_price_change / average_input_candle_price) * 100
        training_output[i] = classify_percentage_change(percent_change)
    return { 'input': training_input, 'output': training_output }

def classify_percentage_change(change):
    if change < -13:
        return 0
    elif change < -8:
        return 1
    elif change < -4.5:
        return 2
    elif change < -1:
        return 3
    elif change < 1:
        return 4
    elif change < 4.5:
        return 5
    elif change < 8:
        return 6
    elif change >= 8:
        return 7

def get_input_for_candle(candle, symbol):
    return [
        get_symbol_id(symbol),
        candle['time'],
        candle['open'],
        candle['close'],
        candle['high'],
        candle['low'],
        candle['volume']
    ]

def get_most_recent_input_data(symbol):
    candle_data = get_candle_data(symbol)
    size = len(candle_data)
    candle = candle_data[size-1]
    return get_input_for_candle(candle, symbol)

def get_symbol_id(symbol):
    return int.from_bytes(symbol.encode(), 'little')
    
    