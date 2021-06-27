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
from datetime import datetime
import backtrader as bt

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

################### backtesting #########################
class SmaCross(bt.Strategy): # bt.Strategy를 상속한 class로 생성해야 함.
    params = dict(
        pfast=5, # period for the fast moving average
        pslow=30 # period for the slow moving average
    )
    
    def __init__(self):
        sma1 = bt.ind.SMA(period=self.p.pfast) # fast moving average
        sma2 = bt.ind.SMA(period=self.p.pslow) # slow moving average
        self.crossover = bt.ind.CrossOver(sma1, sma2) # crossover signal

    def next(self):
        if not self.position: # not in the market
            if self.crossover > 0: # if fast crosses slow to the upside
                close = self.data.close[0] # 종가 값
                size = int(self.broker.getcash() / close) # 최대 구매 가능 개수
                self.buy(size=size) # 매수 size = 구매 개수 설정
            elif self.crossover < 0: # in the market & cross to the downside
                self.close() # 매도

def run_backtesting(data):
    cerebro = bt.Cerebro() # create a "Cerebro" engine instance
    #data = bt.feeds.YahooFinanceData(dataname='005930.KS', fromdate=datetime(2019, 1, 1), todate=datetime(2019, 12, 31))
    cerebro.adddata(data)
    cerebro.broker.setcash(1000000) # 초기 자본 설정
    cerebro.broker.setcommission(commission=0.00015) # 매매 수수료는 0.015% 설정
    cerebro.addstrategy(SmaCross) # 자신만의 매매 전략 추가
    cerebro.run() # 백테스팅 시작
    cerebro.plot() # 그래프로 보여주기

############################################################################

def time_now():
    now = time.localtime()
    current_time = ( str(now.tm_year)+str(now.tm_mon).zfill(2)+str(now.tm_mday).zfill(2)+str(now.tm_hour).zfill(2)+str(now.tm_min).zfill(2)+str(now.tm_sec).zfill(2) )
    return current_time

def tickers_load_all(std_price):
    tickers = pyupbit.get_tickers(fiat=std_price) # KRW/BTC/USDT
    return tickers

def get_mass_candle(name = "BTC", interval = "d", cnt = 10):
    """ 
    param name : "KRW-"제외한 코인명 ex) BTC, ETH, XRP, ...
    param interval : d, m1, m3, m5, m10, m15, m30, m60, m240, w, m
    param cnt :  cnt * 200봉 - 가져올 캔들의 200봉의 배수
    """
    candle_units = {"m1":"minutes1", "m3":"minutes3", "m5":"minutes5", "m10":"minutes10",
                    "m15":"minutes15", "m30":"minutes30", "m60":"minutes60",
                    "m240":"minutes240", "d":"days", "w":"weeks", "m":"months"}

    t = time.time()

    # 최근 200봉 데이터 획득
    df = pyupbit.get_ohlcv("KRW-" + name, interval = candle_units[interval])
    
    # REST API 요청 수 제한
    # 분당 600회, 초당 10회 (종목, 캔들, 체결, 티커, 호가별)

    # 마지막 데이터 이전데이터 200봉 획득 cnt만큼 반복하여 df에 병합
    while cnt > 1:
        df2 = pyupbit.get_ohlcv("KRW-" + name, interval = candle_units[interval], to = df.index[0])
        if df2 is None: # 요청 수 제한 초과시 재시도 예외 처리
            print("Request Time Error")
            time.sleep(1)
            continue
        df = pd.concat([df2,df])
        cnt -= 1
        time.sleep(0.05)

    df.reset_index(inplace=True) # index 리셋
    df.rename(columns={"index":"date"}, inplace = True) # 열이름 date 변경

    print("Get Data Time :", time.time()-t)

    return df

def to_excel(df, filename="test"):
    """
    param df : 데이터프레임
    param filename : 확장자를 제외한 파일명(문자열)
    """
    t = time.time()

    df.set_index("date", inplace=True) # date 를 index로 설정
    df = df.reindex(index = df.index[::-1]) # 최근 데이터가 위쪽으로 올라오도록
    df.reset_index(inplace=True) # index 추가
    df.to_excel(filename + ".xlsx", float_format = "%.4f")

    print("Save Time :", time.time()-t)

    return 0

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
    bb_upper, bb_middle, bb_lower = talib.BBANDS(array_from_df, 20, 2, 2)
    df['RSI'] = rsi
    df['MACD'] = macd
    df['MACD_SIG'] = macdsig
    df['MACD_HISTO'] = macdhisto
    df['BBDANDS_UPPER'] = bb_upper
    df['BBDANDS_MIDDLE'] = bb_middle
    df['BBDANDS_LOWER'] = bb_lower
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

def search_dataframe(df, ticker):
    is_cointype = df['TICKER'] == 'KRW-XRP'
    return df[is_cointype]

def login():
    ext_key = open("ext_key", 'r')
    access_key = ext_key.readline()[:-1]
    secret_key = ext_key.readline()[:-1]
    ext_key.close()
    key = pyupbit.Upbit(access_key, secret_key)
    return key

def buy_limit_stock(key, ticker, price, quantity):
    return key.buy_limit_order(ticker, price, quantity)

def buy_market_stock(key, ticker, market_price):
    return key.buy_market_order(ticker, market_price)

def sell_limit_stock(key, ticker, price, quantity):
    return key.sell_limit_order(ticker, price, quantity)

def sell_market_stock(key, ticker, quantity):
    return key.sell_market_order(ticker, quantity)

def cancle_order(key, uuid):
    return key.cancel_order('uuid')

def get_balance(key, ticker):
    return key.get_balance(ticker)

def get_balances(key):
    return key.get_balances()

def check_condition(key, ticker):
    status = 0
    balances = get_balances(key)
    for balance in balances:
        have = ('KRW-'+balance['currency'])
        small = balance['balance']
        if( (have==ticker) and (float(small)>0.035) ): # tmp ETH only
            #print("Have "+ticker)
            status |= 1
        else:
            #print("None "+ticker)
            status |= 0
    return status

def strategy(key, df, status):
    ticker = df['TICKER'].iloc[-1:][0]
    buy_price = list(df['RSI'].iloc[-1:])[0]
    sell_price = list(df['RSI'].iloc[-1:])[0]
    buy_flag = status["buy_flag"]
    sell_flag = status["sell_flag"]

    if (buy_price < 30) and (buy_price >= 20) and (buy_flag == 0):
        status["buy_flag"] = 1
        buy = buy_market_stock(key, ticker, 10000)
        print(buy)
        print(time_now(), end='')
        print(" Buy "+ticker+ " Success")
        print(df.iloc[-1:])
    elif (buy_price < 20) and (buy_price >= 10) and (buy_flag == 1):
        status["buy_flag"] = 2
        buy = buy_market_stock(key, ticker, 20000)
        print(buy)
        print(time_now(), end='')
        print(" Buy "+ticker+ " Success")
        print(df.iloc[-1:])
    elif (buy_price < 10) and (buy_price >= 0) and (buy_flag == 2):
        status["buy_flag"] = 3
        buy = buy_market_stock(key, ticker, 40000)
        print(buy)
        print(time_now(), end='')
        print(" Buy "+ticker+ " Success")
        print(df.iloc[-1:])
    elif (buy_price > 50):
        status["buy_flag"] = 0
    else:
        pass

    balance = get_balance(key, ticker)
    if (sell_price > 70) and (sell_flag == 0):
        if(balance == 0):
            print(time_now(), end='')
            print(" Dont have  "+ticker)
        else:
            status["sell_flag"] = 1
            sell = sell_market_stock(key, ticker, (balance/2))
            print(sell)
            print(time_now(), end='')
            print(" Sell "+ticker+ " Success")
            print(df.iloc[-1:])
    elif (sell_price > 70) and (sell_flag == 1):
        status["sell_flag"] = 2
        sell = sell_market_stock(key, ticker, balance/2)
        print(sell)
        print(time_now(), end='')
        print(" Sell "+ticker+ " Success")
        print(df.iloc[-1:])
    elif (sell_price > 70) and (sell_flag == 2):
        status["sell_flag"] = 3
        sell = sell_market_stock(key, ticker, balance)
        print(sell)
        print(time_now(), end='')
        print(" Sell "+ticker+ " Success")
        print(df.iloc[-1:])
    elif (sell_price < 50):
        status["sell_flag"] = 0
    else:
        pass


def main():
    date = time_now() #'20210503070000' # 년월일시분일초
    count = 200
    interval = "minute1" # minute1~minute60
    std_price = 'close'
    status = {"buy_flag":0, "sell_flag":0}
    #tickers = tickers_load_all('KRW')

    key = login()
    while(1) : 
        date = time_now()
        df = coin_db_load('KRW-ETH', date, count, interval, std_price)
        strategy(key, df, status)
        time.sleep(1)

if __name__ == "__main__":
    main()

