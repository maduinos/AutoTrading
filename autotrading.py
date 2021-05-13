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

def tickers_load_all(std):
    tickers = pyupbit.get_tickers(fiat=std) # KRW/BTC/USDT
    #current_price = pyupbit.get_current_price(tickers)
    #current_price = pd.Series(current_price)
    return tickers

def rsi_load(coin_type, date, count, interval, std):
    df = pyupbit.get_ohlcv(coin_type, to=date, count=count, interval=interval)
    array_from_df = df[std].values
    rsi = talib.RSI(array_from_df)

    return rsi[-1].tolist()

def rsi_read_dataframe(tickers, date, count, interval, std):
    rsi_list = []
    progressbar = ''
    for coin_type in tickers:
        rsi = rsi_load(coin_type, date, count, interval, std)
        rsi_list.append([coin_type, rsi])
        time.sleep(0.05)
        progressbar += ('#')
        os.system('clear')
        print(progressbar,end='\r')

    print('');
    df = pd.DataFrame(rsi_list)
    df.columns = ['COIN_TYPE', 'CURRENT_RSI']
        
    return df 

def search_dataframe(df, coin_type):
    is_cointype = df['COIN_TYPE'] == 'KRW-XRP'
    return df[is_cointype]

def main():
    #date = '20210503070000' # 년월일시분일초
    date = time_now()
    count = 100
    interval = "day" # minute1~minute60
    std = 'close'

    tickers = tickers_load_all('KRW')
    df = rsi_read_dataframe(tickers, date, count, interval, std)
    print(df)
    print(search_dataframe(df, 'KRW-XRP'))

if __name__ == "__main__":
    main()

