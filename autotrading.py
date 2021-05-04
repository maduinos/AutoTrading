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

tickers = pyupbit.get_tickers(fiat="KRW")
current_price = pyupbit.get_current_price(tickers)
current_price = pd.Series(current_price)

def rsi_load(coin_type, date, count, interval, std):
    df = pyupbit.get_ohlcv(coin_type, to=date, count=count, interval=interval)
    df = pd.DataFrame(df)
    print(df)
    print(df[std].iloc[0])

    df['up'] = df[std] - df[std].iloc[0]
    df['down'] = df[std] - df[std].iloc[0]

    df.loc[df.up<0,'up']=0
    df.loc[df.down>0,'down']=0

    close_up_sum = df['up'].sum()
    close_down_sum = df['down'].sum()

    print("close up sum = {}".format(close_up_sum) )
    print("close down sum = {}".format(close_down_sum) )

    rsi = close_up_sum / (close_up_sum + abs(close_down_sum) )
    print("%s RSI = %0.5f"% (coin_type, rsi) )
    return rsi


if __name__ == "__main__":
    coin_type = 'KRW-XRP'
    date = '20210503070000' # 년월일시분일초
    count = 200 
    interval = 'minute1'
    std = 'close'

    rsi = rsi_load(coin_type, date, count, interval, std)
    print(rsi)

