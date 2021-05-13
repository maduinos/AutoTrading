import talib
import numpy as np

close = np.random.random(100)
print(type(close))

rsi = talib.RSI(close)
print(type(rsi))
print(rsi)

