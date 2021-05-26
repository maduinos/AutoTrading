from backtesting import Backtest, Strategy
from backtesting.lib import crossover
from backtesting.test import SMA, GOOG
import FinanceDataReader as fdr

'''
- 전략 설명
10일 이동평균선이 20일 이동평균선을 돌파하면 매수!
20일 이동평균선이 10일 이동평균선을 돌파하면 매도!
'''
class SmaCross(Strategy):
    n1 = 10
    n2 = 20

    def init(self):
        close = self.data.Close
        self.sma1 = self.I(SMA, close, self.n1)
        self.sma2 = self.I(SMA, close, self.n2)

    def next(self):
        if crossover(self.sma1, self.sma2):
            self.buy()
        elif crossover(self.sma2, self.sma1):
            self.sell()


# 셀트리온, 2018년~2019년6월
data = fdr.DataReader('068270', '20180104','20190630')
print(data.head())

# 초기투자금 10000, commission 비율 0.002 임의 지정
bt = Backtest(data, SmaCross,
              cash=10000, commission=.002,
              exclusive_orders=True)

'''
bt = Backtest(GOOG, SmaCross,
              cash=10000, commission=.002,
              exclusive_orders=True)
'''

output = bt.run()
print(output)
bt.plot()

