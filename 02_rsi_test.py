import pyupbit

'''tickers KRW only'''
tickers = pyupbit.get_tickers(fiat="KRW")
print(tickers)
print("=======================================================")

'''현재가 여러종목  조회'''
'''price = pyupbit.get_current_price(["KRW-BTC", "KRW-XRP"])'''
price = pyupbit.get_current_price(tickers)
print(price)
print("=======================================================")

'''시가(open), 고가(high), 저가(low), 종가(close), 거래량(volume) def=일봉'''
df = pyupbit.get_ohlcv("KRW-BTC")
print(df)
print("=======================================================")

'''분봉'''
df = pyupbit.get_ohlcv("KRW-BTC", interval="minute1")
print(df)
print("=======================================================")

'''최근 5일'''
df = pyupbit.get_ohlcv("KRW-BTC", count=5, interval="minute1")
print(df)
print("=======================================================")

''' 10호가 정보'''
orderbook = pyupbit.get_orderbook("KRW-BTC")
bids_asks = orderbook[0]['orderbook_units']

for bid_ask in bids_asks:
    print(bid_ask)
print("=======================================================")

'''잔고 조회'''
access_key = "access_key"
secret_key = "secret_key"
upbit = pyupbit.Upbit(access_key, secret_key)
balances = upbit.get_balances()
print(balances)
print("=======================================================")

'''매수/매도/취소'''
buy = upbit.buy_limit_order("KRW-XRP", 100, 20)
sell = upbit.sell_limit_order("KRW-XRP", 2000, 20)
cancel = upbit.cancel_order('uuid')
print("=======================================================")

