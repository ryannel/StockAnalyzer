import dataprovider
import backtrader


class TestStrategy(backtrader.Strategy):
    def __init__(self):
        self.bar_executed = None

        backtrader.indicators.MovingAverageSimple(self.data.close, period=5)
        # Indicators for plotting
        backtrader.indicators.ExponentialMovingAverage(self.datas[0], period=25)
        backtrader.indicators.WeightedMovingAverage(self.datas[0], period=25).subplot = True
        backtrader.indicators.StochasticSlow(self.datas[0])
        backtrader.indicators.MACDHisto(self.datas[0])
        rsi = backtrader.indicators.RSI(self.datas[0])
        backtrader.indicators.SmoothedMovingAverage(rsi, period=10)
        backtrader.indicators.ATR(self.datas[0]).plot = False

    def log(self, txt):
        date_time = self.data.datetime.date(0)
        print('%s: %s' % (date_time.isoformat(), txt))

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' % (trade.pnl, trade.pnlcomm))

    def notify_order(self, order):
        # Check if an order has been completed
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log('BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' % (
                    order.executed.price, order.executed.value, order.executed.comm))

            else:  # Sell
                self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' % (
                    order.executed.price, order.executed.value, order.executed.comm))

            self.bar_executed = len(self)

        if order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

    def next(self):
        # Simply log the closing price of the series from the reference
        self.log('Close, %.2f' % self.data.close[0])

        # Check if we are in the market
        if not self.position:

            # Not yet ... we MIGHT BUY if ...
            if self.data.close[0] < self.data.close[-1]:
                # current close less than previous close

                if self.data.close[-1] < self.data.close[-2]:
                    # previous close less than the previous close

                    # BUY, BUY, BUY!!! (with default parameters)
                    self.log('BUY CREATE, %.2f' % self.data.close[0])

                    self.buy()

        else:
            # Already in the market ... we might sell
            if len(self) >= (self.bar_executed + 5):
                # SELL, SELL, SELL!!! (with all possible default parameters)
                self.log('SELL CREATE, %.2f' % self.data.close[0])

                self.sell()


def run(history):
    cerebro = backtrader.Cerebro()

    data = backtrader.feeds.PandasData(dataname=history)
    cerebro.adddata(data)
    cerebro.addstrategy(TestStrategy)
    cerebro.broker.setcommission(commission=0.001)  # Broker commission charges for buy and sell
    cerebro.broker.setcash(100000.0)  # Starting funds for the back test
    cerebro.addsizer(backtrader.sizers.FixedSize, stake=10)  # Add a FixedSize sizer according to the stake

    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())  # Print out the starting conditions
    cerebro.run()
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())  # Print the final result

    # cerebro.plot(style='bar')