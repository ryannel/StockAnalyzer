from backtesting import Backtest, Strategy
from backtesting.lib import crossover
from backtesting.test import SMA
import dataprovider


class SmaCross(Strategy):
    def init(self):
        close = self.data.Close
        self.sma1 = self.I(SMA, close, 10)
        self.sma2 = self.I(SMA, close, 20)

    def next(self):
        if crossover(self.sma1, self.sma2):
            self.buy()
        elif crossover(self.sma2, self.sma1):
            self.sell()


def main():
    netflix = dataprovider \
        .DataProvider('nasdaqTradedCompanies.jsonl') \
        .get_company('NASDAQ', 'NFLX')

    history = netflix.get_dataframe()

    bt = Backtest(history, SmaCross, cash=10000, commission=.002)
    output = bt.run()
    bt.plot()
    print(output)


if __name__ == "__main__":
    main()
