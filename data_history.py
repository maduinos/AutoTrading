import requests
import pandas as pd

from bs4 import BeautifulSoup

coin_list = ['BTC', 'ETH', 'BSV', 'XRP', 'BCH', 'EOS']
time_units = ['days', 'weeks']
minutes_units = [1, 3, 5, 15, 30, 60, 240]
'''
'Time'                : 시간 
'OpeningPrice'        : 시가
'HighPrice'           : 고가
'LowPrice'            : 저가
'TradePrice'          : 체결가
'CandleAccTradeVolume': 누적 거래량
'candleAccTradePrice' : 누적 체결가

'''
for coin in coin_list:
    for time_unit in time_units:

        req = requests.get(f'https://crix-api-endpoint.upbit.com/v1/crix/candles/{time_unit}?code=CRIX.UPBIT.KRW-{coin}&count=100&')
        data = req.json()
        result = []

        for i, candle in enumerate(data):
            result.append({
                'Time': data[i]["candleDateTimeKst"],
                'OpeningPrice': data[i]["openingPrice"],
                'HighPrice': data[i]["highPrice"],
                'LowPrice': data[i]["lowPrice"],
                'TradePrice': data[i]["tradePrice"],
                'CandleAccTradeVolume': data[i]["candleAccTradeVolume"],
                'candleAccTradePrice': data[i]["candleAccTradePrice"]
            })
        coin_data = pd.DataFrame(result)
        coin_data.to_csv(f'C:/Users/nalbi/Documents/AutoTrading-main/data/{coin}_KRW_{time_unit}.csv')

    for minutes_unit in minutes_units:

        req = requests.get(f'https://crix-api-endpoint.upbit.com/v1/crix/candles/minutes/{minutes_unit}?code=CRIX.UPBIT.KRW-{coin}&count=400&')
        data = req.json()
        result = []

        for i, candle in enumerate(data):
            result.append({
                'Time': data[i]["candleDateTimeKst"],
                'OpeningPrice': data[i]["openingPrice"],
                'HighPrice': data[i]["highPrice"],
                'LowPrice': data[i]["lowPrice"],
                'TradePrice': data[i]["tradePrice"],
                'CandleAccTradeVolume': data[i]["candleAccTradeVolume"],
                'candleAccTradePrice': data[i]["candleAccTradePrice"]
            })
        coin_data = pd.DataFrame(result)
        coin_data.to_csv(f'C:/Users/nalbi/Documents/AutoTrading-main/data/{coin}_KRW_{minutes_unit}.csv')