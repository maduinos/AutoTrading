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

