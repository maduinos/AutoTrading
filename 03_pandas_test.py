import pyupbit
import pandas as pd
import numpy as np
import time

tickers = pyupbit.get_tickers(fiat="KRW")
#print(tickers)
#current_price = pyupbit.get_current_price("KRW-XRP")
current_price = pyupbit.get_current_price(tickers)
current_price = pd.Series(current_price)
#print(current_price)

coin_type = "KRW-XRP"

df = pyupbit.get_ohlcv(coin_type, count=200, interval="minute1")
df = pd.DataFrame(df)
print(df)

print(df['close'].iloc[0])

df['up'] = df['close'] - df['close'].iloc[0]
df['down'] = df['close'] - df['close'].iloc[0]
print(df)

df.loc[df.up<0,'up']=0
df.loc[df.down>0,'down']=0
print(df)

close_up_sum = df["up"].sum()
close_down_sum = df["down"].sum()
print("close up sum = {}".format(close_up_sum) )
print("close down sum = {}".format(close_down_sum) )

rsi = close_up_sum / (close_up_sum + abs(close_down_sum) )
print("%s RSI = %0.5f"% (coin_type, rsi) )

print(df.describe())

now = time.localtime()
print("%04d%02d%02d%02d%02d%02d"%(now.tm_year,now.tm_mon,now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec) )
print( str(now.tm_year)+str(now.tm_mon).zfill(2)+str(now.tm_mday).zfill(2)+str(now.tm_hour).zfill(2)+str(now.tm_min).zfill(2)+str(now.tm_sec).zfill(2) )

#Git Trans Test
