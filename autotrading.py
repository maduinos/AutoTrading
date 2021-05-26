"""-----------------------------------------------------------------------
* MODIFICATION HISTORY
* Ver    Who       Date         Changes
* ----- --------- ---------- --------------------------------------------
* 0.0.1  maduinos  2021/05/04   First release
* 0.0.2  maduinos  2021/05/13   Used TA-Lib
*
-----------------------------------------------------------------------"""

import pyupbit
import talib
import pandas as pd
import numpy as np
import time
import os
import sys

buy_flag = 0

def time_now():
    now = time.localtime()
    current_time = ( str(now.tm_year)+str(now.tm_mon).zfill(2)+str(now.tm_mday).zfill(2)+str(now.tm_hour).zfill(2)+str(now.tm_min).zfill(2)+str(now.tm_sec).zfill(2) )
    return current_time

def tickers_load_all(std_price):
    tickers = pyupbit.get_tickers(fiat=std_price) # KRW/BTC/USDT
    return tickers

def add_current_price(coin_type, df):
    current_price = pyupbit.get_current_price(coin_type)
    df['COIN_TYPE'] = coin_type
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

def coin_data_load(coin_type, date, count, interval, std_price):
    df = pyupbit.get_ohlcv(coin_type, to=date, count=count, interval=interval)
    #df.set_index('COIN_TYPE')
    return df

def coin_db_load(coin_type, date, count, interval, std_price):
    coin_data_df = coin_data_load(coin_type, date, count, interval, std_price)
    analysis_df = analysis_load(coin_data_df, std_price)
    df = add_current_price(coin_type, analysis_df)
    df = change_columns(df)
    return df 

'''
def analysis_read(tickers, date, count, interval, price):
    analysis_df_list = pd.DataFrame([])
    progressbar = ''
    for coin_type in tickers:
        current_price = pyupbit.get_current_price(coin_type)
        coin_data_df = coin_data_load(coin_type, date, count, interval, price)
        analysis_df = analysis_load(coin_data_df, price)
        analysis_df['COIN_TYPE'] = coin_type
        analysis_df['CUR_PRICE'] = current_price

        analysis_df_list(analysis_df.iloc[-1:,:])
        print(analysis_df_list)

        time.sleep(0.05)
        progressbar += ('#')
        os.system('clear')
        print(progressbar,end='\r')

    print('');
    analysis_df_list.set_index('COIN_TYPE')
    print(analysis_df_list)
        
    return analysis_df_list
'''

def search_dataframe(df, coin_type):
    is_cointype = df['COIN_TYPE'] == 'KRW-XRP'
    return df[is_cointype]

def login():
    access_key = "access_key"
    secret_key = "secret_key"
    key = pyupbit.Upbit(access_key, secret_key)
    return key

def buy_limit_stock(key, coin_type, price, quantity):
    return key.buy_limit_order(coin_type, price, quantity)

def buy_market_stock(key, coin_type, price):
    return key.buy_market_order(coin_type, price)

def sell_limit_stock(key, coin_type, price, quantity):
    return key.sell_limit_order(coin_type, price, quantity)

def sell_market_stock(key, coin_type, quantity):
    return key.sell_market_order(coin_type, quantity)

def cancle_order(key, uuid):
    return key.cancel_order('uuid')

def tmp_xrp_strategy(key, df):
    if (list(df['RSI'].iloc[-1:])[0]) < 30 :
        buy = buy_market_stock(key, 'KRW-DOGE', 20000)
        print(buy)
        buy_flag = 1
    elif (list(df['RSI'].iloc[-1:])[0]) > 70 :
        sell = sell_market_stock(key, 'KRW-DOGE', 30)
        print(sell)
        buy_flag = 0

buy_flag = 0
def main():
    #date = '20210503070000' # 년월일시분일초
    date = time_now()
    count = 200
    interval = "minute1" # minute1~minute60
    std_price = 'close'

    #tickers = tickers_load_all('KRW')

    key = login()
    while(1) : 
        date = time_now()
        df = coin_db_load('KRW-DOGE', date, count, interval, std_price)
        tmp_xrp_strategy(key, df)
        print(df['RSI'].iloc[-1:])
        time.sleep(10)

if __name__ == "__main__":
    main()

