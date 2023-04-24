from backtesting import Backtest, Strategy
from pricing import Pricing
from KNN import Knnpredictor_2020_after
from KNN_2020 import Knnpredictor_2020_before

class Crosscurrency():
    def __init__(self):
        pass

    def run_():

        import pandas as pd
        df = pd.read_csv("/Volumes/SeagateExpansion/dataForex_trades/CADUSD_day.csv")
        # df = pd.read_csv("/Volumes/SeagateExpansion/dataForex/ETHUSD_day.csv")

        df.head()

        start_date = '2013-07-01'
        end_date = '2022-04-30'
        mask = (df['t'] > start_date) & (df['t'] <= end_date)
        df = df.loc[mask]

        df.shape

        df['Open'] = df['o'] 
        df['High'] = df['h'] 
        df['Low'] = df['l'] 
        df['Close'] = df['c'] 
        df['Volume'] = df['v'] 

        df2 = df[['Open','High','Low', 'Close', 'Volume']]
        df2.index = pd.to_datetime((df['t']))

        df2.tail()

        from backtesting import Backtest, Strategy
        from backtesting.lib import crossover

        from backtesting.test import SMA, GOOG

        class SmaCross(Strategy):
            def init(self):
                price = self.data.Close
                self.ma1 = self.I(SMA, price,3)
                self.ma2 = self.I(SMA, price,20)

            def next(self):
                if crossover(self.ma1, self.ma2):
                    self.buy()
                elif crossover(self.ma2, self.ma1):
                    self.sell()


        import warnings
        warnings.filterwarnings(action='once')
        warnings.simplefilter(action='ignore', category=FutureWarning)


        bt = Backtest(df2, SmaCross, cash = 10000,commission=.002,
                      exclusive_orders=True)
        stats = bt.run()
        # bt.plot()
        s3 = bt.plot()
        return stats,s3
        