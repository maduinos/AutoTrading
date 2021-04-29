import pyupbit

'''tickers all'''
tickers = pyupbit.get_tickers() 
print(tickers)

'''tickers KRW only'''
tickers = pyupbit.get_tickers(fiat="KRW")
print(tickers)

'''현재가 조회'''
current_price = pyupbit.get_current_price("KRW-XRP")
print(current_price)

'''현재가 여러종목  조회'''
price = pyupbit.get_current_price(["BTC-XRP", "KRW-XRP"])
print(price)

'''시가(open), 고가(high), 저가(low), 종가(close), 거래량(volume) def=일봉'''
df = pyupbit.get_ohlcv("KRW-BTC")
print(df)

'''분봉??'''
df = pyupbit.get_ohlcv("KRW-BTC", interval="minute")
print(df)

'''최근 5일'''
df = pyupbit.get_ohlcv("KRW-BTC", count=5)
print(df)

'''매수호가 매도호가'''
orderbook = pyupbit.get_orderbook("KRW-BTC")
print(orderbook)

''' 10호가 정보'''
orderbook = pyupbit.get_orderbook("KRW-BTC")
bids_asks = orderbook[0]['orderbook_units']

for bid_ask in bids_asks:
    print(bid_ask)

'''잔고 조회'''
access_key = "access_key"
secret_key = "secret_key"
upbit = pyupbit.Upbit(access_key, secret_key)
balances = upbit.get_balances()
print(balances)

'''매수/매도/취소'''
buy = upbit.buy_limit_order("KRW-XRP", 100, 20)
sell = upbit.sell_limit_order("KRW-XRP", 2000, 20)
cancel = upbit.cancel_order('uuid')


