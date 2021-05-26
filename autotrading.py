"""-----------------------------------------------------------------------
* MODIFICATION HISTORY
* Ver    Who       Date         Changes
* ----- --------- ---------- --------------------------------------------
* 0.0.1  maduinos  2021/05/04   First release
* 0.0.2  maduinos  2021/05/13   Used TA-Lib
* 0.0.3  hskim     2021/05/26   add history data load
*
-----------------------------------------------------------------------"""

import time
import os
import sys
import pyupbit
import talib
import pandas as pd
import numpy as np

def time_now():
    now = time.localtime()
    current_time = ( str(now.tm_year)+str(now.tm_mon).zfill(2)+str(now.tm_mday).zfill(2)+str(now.tm_hour).zfill(2)+str(now.tm_min).zfill(2)+str(now.tm_sec).zfill(2) )
    return current_time

def tickers_load_all(std_price):
    tickers = pyupbit.get_tickers(fiat=std_price) # KRW/BTC/USDT
    return tickers

def history_data_load(ticker, interval, cnt) :
    # 최근 200봉 데이터 획득
    df = pyupbit.get_ohlcv(ticker, interval=interval)
    #df = df.reindex(index=df.index[::-1]) # 최근 데이터가 위쪽으로 올라오도록
    t = time.time()

    # REST API 요청 수 제한
    # 분당 600회, 초당 10회 (종목, 캔들, 체결, 티커, 호가별)
    # 마지막 데이터 이전데이터 200봉 획득
    for i in range(cnt):
        df2 = pyupbit.get_ohlcv(ticker, interval=interval, to=df.index[0])
        if df2 is None: # 요청 수 제한 초과시 재시도 예외 처리
            # print("Request Time Error")
            time.sleep(0.5)
            continue
        # df2 = df2.reindex(index=df2.index[::-1]) # 최근 데이터가 위쪽으로 올라오도록
        df = pd.concat([df2,df])
        # time.sleep(0.05)

    df.reset_index(inplace=True) # index 리셋
    df.rename(columns={'index':'date'}, inplace=True) # 열이름 date 변경
    # print(df)
    print("Get Data Time :", time.time()-t)
    t = time.time()
    df.to_excel("mass_data.xlsx")
    print("Save Time :", time.time()-t)

def add_current_price(ticker, df):
    current_price = pyupbit.get_current_price(ticker)
    df['TICKER'] = ticker
    df['CUR_PRICE'] = current_price
    return df

def change_columns(df):
    col1=df.columns[-2:].to_list()
    col2=df.columns[:-2].to_list()
    new_col=col1+col2
    df=df[new_col]
    return df

def analysis_load(df, std_price):
    array_from_df = df[std_price].values
    rsi = talib.RSI(array_from_df)
    macd, macdsig, macdhisto = talib.MACD(array_from_df)
    df['RSI'] = rsi
    df['MACD'] = macd
    df['MACD_SIG'] = macdsig
    df['MACD_HISTO'] = macdhisto
    return df

def coin_data_load(ticker, date, count, interval, std_price):
    df = pyupbit.get_ohlcv(ticker, to=date, count=count, interval=interval)
    #df.set_index('TICKER')
    return df

def coin_db_load(ticker, date, count, interval, std_price):
    coin_data_df = coin_data_load(ticker, date, count, interval, std_price)
    analysis_df = analysis_load(coin_data_df, std_price)
    df = add_current_price(ticker, analysis_df)
    df = change_columns(df)
    return df 

'''
def analysis_read(tickers, date, count, interval, price):
    analysis_df_list = pd.DataFrame([])
    progressbar = ''
    for ticker in tickers:
        current_price = pyupbit.get_current_price(ticker)
        coin_data_df = coin_data_load(ticker, date, count, interval, price)
        analysis_df = analysis_load(coin_data_df, price)
        analysis_df['ticker'] = ticker
        analysis_df['CUR_PRICE'] = current_price

        analysis_df_list(analysis_df.iloc[-1:,:])
        print(analysis_df_list)

        time.sleep(0.05)
        progressbar += ('#')
        os.system('clear')
        print(progressbar,end='\r')

    print('');
    analysis_df_list.set_index('ticker')
    print(analysis_df_list)
        
    return analysis_df_list
'''

def search_dataframe(df, ticker):
    is_cointype = df['TICKER'] == 'KRW-XRP'
    return df[is_cointype]

def login():
    access_key = "access_key"
    secret_key = "secret_key"
    key = pyupbit.Upbit(access_key, secret_key)
    return key

def buy_limit_stock(key, ticker, price, quantity):
    return key.buy_limit_order(ticker, price, quantity)

def buy_market_stock(key, ticker, quantity):
    return key.buy_market_order(ticker, quantity)

def sell_limit_stock(key, ticker, price, quantity):
    return key.sell_limit_order(ticker, price, quantity)

def sell_market_stock(key, ticker, quantity):
    return key.sell_market_order(ticker, quantity)

def cancle_order(key, uuid):
    return key.cancel_order('uuid')

def get_balance(key, ticker):
    return key.get_balance(ticker)['balance']

def my_strategy(key, df):
    return 0

def main():
    #date = '20210503070000' # 년월일시분일초
    date = time_now()
    count = 100
    interval = "day" # minute1~minute60
    std_price = 'close'

    #tickers = tickers_load_all('KRW')
    df = coin_db_load('KRW-BTC', date, count, interval, std_price)
    print(df.iloc[-1:,:])
    #print(df)

if __name__ == "__main__":
    main()

