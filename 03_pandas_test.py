import pyupbit
import pandas as pd
import numpy as np

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
