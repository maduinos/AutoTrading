"""-----------------------------------------------------------------------
* MODIFICATION HISTORY
* Ver    Who       Date         Changes
* ----- --------- ---------- --------------------------------------------
* 0.0.1  maduinos  2021/05/04   First release
*
-----------------------------------------------------------------------"""

import pyupbit
import pandas as pd
import numpy as np
import time
import os

tickers = pyupbit.get_tickers(fiat="KRW")
current_price = pyupbit.get_current_price(tickers)
current_price = pd.Series(current_price)

def rsi_load(coin_type, date, count, interval, std):
    df = pyupbit.get_ohlcv(coin_type, to=date, count=count, interval=interval)
    df = pd.DataFrame(df)
    #print(df[std].iloc[0])

    df['up'] = df[std] - df[std].iloc[0]
    df['down'] = df[std] - df[std].iloc[0]

    df.loc[df.up<0,'up']=0
    df.loc[df.down>0,'down']=0
    #print(df)

    up_sum = df['up'].sum()
    down_sum = abs(df['down'].sum())
    #print("close up sum = {}".format(up_sum) )
    #print("close down sum = {}".format(down_sum) )

    rsi = up_sum / (up_sum + down_sum)
    return rsi

def rsi_dataframe(coin_type, date, count, interval, std):
    rsi_list = []
    progressbar = ''
    for coin in tickers:
        rsi = rsi_load(coin, date, count, interval, std)
        rsi_list.append([coin, rsi])
        #print("%s RSI = %0.5f"% (coin, rsi) )
        time.sleep(0.1)
        progressbar += ('#')
        os.system('clear')
        print(progressbar,end='\r')

    print('');
    df = pd.DataFrame(rsi_list)
    df.columns = ['COIN_TYPE', 'RSI_14']
        
    return df 

if __name__ == "__main__":
    now = time.localtime()
    current_time = ( str(now.tm_year)+str(now.tm_mon).zfill(2)+str(now.tm_mday).zfill(2)+str(now.tm_hour).zfill(2)+str(now.tm_min).zfill(2)+str(now.tm_sec).zfill(2) )
    coin_type = 'KRW-GRS'
    #date = '20210503070000' # 년월일시분일초
    date = current_time 
    count = 14 
    #interval = "minute60"
    interval = "day"
    std = 'close'

    df = rsi_dataframe(coin_type, date, count, interval, std)
    print(df)

