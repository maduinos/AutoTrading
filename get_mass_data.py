import pyupbit
import pandas as pd
import time

ticker = "KRW-XRP"
interval = "minutes1"
cnt = 100

# 최근 200봉 데이터 획득
df = pyupbit.get_ohlcv(ticker, interval=interval)
df = df.reindex(index=df.index[::-1]) # 최근 데이터가 위쪽으로 올라오도록

t = time.time()

# REST API 요청 수 제한
# 분당 600회, 초당 10회 (종목, 캔들, 체결, 티커, 호가별)

# 마지막 데이터 이전데이터 200봉 획득
for i in range(cnt):
    df2 = pyupbit.get_ohlcv(ticker, interval=interval, to=df.index[-1])
    if df2 is None: # 요청 수 제한 초과시 재시도 예외 처리
        # print("Request Time Error")
        time.sleep(0.5)
        continue
    df2 = df2.reindex(index=df2.index[::-1]) # 최근 데이터가 위쪽으로 올라오도록
    df = pd.concat([df,df2])
    # time.sleep(0.05)

df.reset_index(inplace=True) # index 리셋
df.rename(columns={'index':'date'}, inplace=True) # 열이름 date 변경

# print(df)

print("Get Data Time :", time.time()-t)

t = time.time()

df.to_excel("mass_data.xlsx")

print("Save Time :", time.time()-t)