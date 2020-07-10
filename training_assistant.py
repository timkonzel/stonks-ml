from stock_service import get_candle_data, get_recommendation_data
import datetime
import math

def format_training_data(symbol):
    candle_data = get_candle_data(symbol)
    recommendation_data = get_recommendation_data(symbol)[::-1]
    size = len(candle_data) - 1;
    training_input = [None] * size;
    training_output = [None] * size;
    for i in range(size):
        input_candle = candle_data[i]
        next_candle = candle_data[i+1]
        training_input[i] = get_input_for_candle(input_candle, symbol, recommendation_data)
        average_input_candle_price = (input_candle['open'] + input_candle['close'] + input_candle['high'] + input_candle['low']) / 4
        average_next_candle_price = (next_candle['open'] + next_candle['close'] + next_candle['high'] + next_candle['low']) / 4
        average_price_change = average_next_candle_price - average_input_candle_price
        percent_change = (average_price_change / average_input_candle_price) * 100
        training_output[i] = classify_percentage_change(percent_change)
    return { 'input': training_input, 'output': training_output }

def classify_percentage_change(change):
    if change < -6:
        return 0
    elif change < -4:
        return 1
    elif change < -2:
        return 2
    elif change < -1:
        return 3
    elif change <= 0:
        return 4
    elif change < 1:
        return 5
    elif change < 2:
        return 6
    elif change < 4:
        return 7
    elif change < 6:
        return 8
    elif change >= 6:
        return 9

def get_input_for_candle(candle, symbol, recommendation_data):
    candle_time = candle['time']
    time_key = datetime.datetime.fromtimestamp(candle_time).strftime('%Y-%m-01')
    recommendation = get_recommendation_with_key(recommendation_data, time_key)
    recommendation_score = get_recommendation_score(recommendation)
    return [
        get_symbol_id(symbol),
        candle_time,
        get_average_candle_price(candle),
        get_candle_percent_change(candle),
        candle['volume'],
        recommendation_score
    ]

def get_most_recent_input_data(symbol):
    candle_data = get_candle_data(symbol)
    size = len(candle_data)
    candle = candle_data[size-1]
    recommendation_data = get_recommendation_data(symbol)
    return get_input_for_candle(candle, symbol, recommendation_data)

def get_symbol_id(symbol):
    return int.from_bytes(symbol.encode(), 'little')
    
def get_average_candle_price(candle):
    return (candle['open'] + candle['close'] + candle['high'] + candle['low']) / 4

def get_candle_percent_change(candle):
    return ((candle['close'] - candle['open']) / candle['open']) * 100

def get_recommendation_with_key(data, time_key):
    for recommendation in data:
        if recommendation.period == time_key:
            return recommendation

def get_recommendation_score(recommendation):
    if recommendation == None:
        return 0
    return ((recommendation.strong_buy * 5) - (recommendation.strong_sell * 10) + (recommendation.buy * 2) + recommendation.hold - (recommendation.sell * 5))
