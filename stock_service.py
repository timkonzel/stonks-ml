import finnhub
import datetime

configuration = finnhub.Configuration(
    api_key={
        'token': 'bs3t7rfrh5r9iotip350'
    }
)

finnhub_client = finnhub.DefaultApi(finnhub.ApiClient(configuration))

def get_candle_data(symbol):
    end_time = int(datetime.datetime.now().timestamp())
    start_time = int((datetime.datetime.now() - datetime.timedelta(days=364)).timestamp())
    response = finnhub_client.stock_candles(symbol, 'D', start_time, end_time)
    length = len(response.t)
    candles = [None] * length
    for x in range(length):
        candles[x] = {
            'open': response.o[x],
            'close': response.c[x],
            'high': response.h[x],
            'low': response.l[x],
            'volume': response.v[x],
            'time': response.t[x] 
        }
    return candles

def get_recommendation_data(symbol):
    return finnhub_client.recommendation_trends(symbol)
    