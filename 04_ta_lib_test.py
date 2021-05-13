import talib
import numpy as np

close = np.random.random(100)
print(close)

rsi = talib.RSI(close)
print(rsi)

