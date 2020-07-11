from stock_service import get_candle_data, get_recommendation_data
import datetime
import math

def format_training_data(symbol):
    candle_data = get_candle_data(symbol)
    recommendation_data = get_recommendation_data(symbol)[::-1]
    size = len(candle_data);
    training_input = [None] * size;
    training_output = [None] * size;
    for i in range(size):
        input_candle = candle_data[i]
        training_input[i] = i
        training_output[i] = input_candle['close']
    return { 'input': training_input, 'output': training_output }

def get_input_for_candle(candle, symbol, recommendation_data):
    candle_time = candle['time']
    time_key = datetime.datetime.fromtimestamp(candle_time).strftime('%Y-%m-01')
    recommendation = get_recommendation_with_key(recommendation_data, time_key)
    recommendation_score = get_recommendation_score(recommendation)
    return candle_time

def get_most_recent_input_data(symbol):
    candle_data = get_candle_data(symbol)
    size = len(candle_data)
    candle = candle_data[size-1]
    recommendation_data = get_recommendation_data(symbol)
    return get_input_for_candle(candle, symbol, recommendation_data)

def get_symbol_id(symbol):
    return int.from_bytes(symbol.encode(), 'little')


def get_recommendation_with_key(data, time_key):
    for recommendation in data:
        if recommendation.period == time_key:
            return recommendation

def get_recommendation_score(recommendation):
    if recommendation == None:
        return 0
    return ((recommendation.strong_buy * 5) - (recommendation.strong_sell * 10) + (recommendation.buy * 2) + recommendation.hold - (recommendation.sell * 5))
