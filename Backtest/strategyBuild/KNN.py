
## Reference: https://github.com/kernc/backtesting.py/tree/master/backtesting

class Knnpredictor_2020_after():
    def __init__(self):
        pass
    def run():
        import pandas as pd
        from backtesting import Backtest, Strategy
        from backtesting.test import SMA
        df = pd.read_csv("../eurusd.csv")
        # df = pd.read_csv("/Volumes/SeagateExpansion/dataForex_trades/USDGBP_day.csv")

        df.head()

        start_date = '2013-11-06'
        end_date = '2022-05-31'
        mask = (df['t'] > start_date) & (df['t'] <= end_date)
        df = df.loc[mask]

        df.shape

        df['Open'] = df['o'] 
        df['High'] = df['h'] 
        df['Low'] = df['l'] 
        df['Close'] = df['c'] 
        df['Volume'] = df['v'] 

        data = df[['Open','High','Low', 'Close', 'Volume']]
        data.index = pd.to_datetime((df['t']))

        data.tail() 
        def BBANDS(data, n_lookback, n_std):
            """Bollinger bands indicator"""
            hlc3 = (data.High + data.Low + data.Close) / 3
            mean, std = hlc3.rolling(n_lookback).mean(), hlc3.rolling(n_lookback).std()
            upper = mean + n_std*std
            lower = mean - n_std*std
            return upper, lower


        close = data.Close.values
        sma10 = SMA(data.Close, 10)
        sma20 = SMA(data.Close, 20)
        sma50 = SMA(data.Close, 50)
        sma100 = SMA(data.Close, 100)
        upper, lower = BBANDS(data, 20, 2)

        # Design matrix / independent features:

        # Price-derived features
        data['X_SMA10'] = (close - sma10) / close
        data['X_SMA20'] = (close - sma20) / close
        data['X_SMA50'] = (close - sma50) / close
        data['X_SMA100'] = (close - sma100) / close

        data['X_DELTA_SMA10'] = (sma10 - sma20) / close
        data['X_DELTA_SMA20'] = (sma20 - sma50) / close
        data['X_DELTA_SMA50'] = (sma50 - sma100) / close

        # Indicator features
        data['X_MOM'] = data.Close.pct_change(periods=2)
        data['X_BB_upper'] = (upper - close) / close
        data['X_BB_lower'] = (lower - close) / close
        data['X_BB_width'] = (upper - lower) / close
        # data['X_Sentiment'] = ~data.index.to_series().between('2017-09-27', '2017-12-14')

        data['X_p10m_median_c'] = data['Close'].rolling(10, min_periods=1).median()
        data['X_p30m_median_c'] = data['Close'].rolling(30, min_periods=1).median()
        data['X_p60m_median_c'] = data['Close'].rolling(60, min_periods=1).median()

        data['X_p10m_std_c'] = data['Close'].rolling(10).std()
        data['X_p30m_std_c'] = data['Close'].rolling(30).std()
        data['X_p60m_std_c'] = data['Close'].rolling(60).std()

        data['X_p10m_skew_c'] = data['Close'].rolling(10).skew()
        data['X_p30m_skew_c'] = data['Close'].rolling(30).skew()
        data['X_p60m_skew_c'] = data['Close'].rolling(60).skew()

        data['X_p10m_kurt_c'] = data['Close'].rolling(10).kurt()
        data['X_p30m_kurt_c'] = data['Close'].rolling(30).kurt()
        data['X_p60m_kurt_c'] = data['Close'].rolling(60).kurt()
        # Some datetime features for good measure
        data['X_day'] = data.index.dayofweek
        data['X_hour'] = data.index.hour

        data = data.dropna().astype(float)

        import numpy as np

        currencyRelativeRate = 0.001 # 0.004 = 0.4%, 0.002 gives good result.

        def get_X(data):
            """Return model design matrix X"""
            return data.filter(like='X').values


        def get_y(data):
            """Return dependent variable y"""
            y = data.Close.pct_change(2).shift(-2)  # Returns after roughly two days/hour
            y[y.between(-currencyRelativeRate, currencyRelativeRate)] = 0             # Devalue returns smaller than 0.4%
            y[y > 0] = 1
            y[y < 0] = -1
            return y


        def get_clean_Xy(df):
            """Return (X, y) cleaned of NaN values"""
            X = get_X(df)
            y = get_y(df).values
            isnan = np.isnan(y)
            X = X[~isnan]
            y = y[~isnan]
            return X, y

        import pandas as pd
        from sklearn.neighbors import KNeighborsClassifier
        from sklearn.model_selection import train_test_split

        # X, y = get_clean_Xy(data)
        # X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.5, random_state=0)

        # clf = KNeighborsClassifier(20)  # Model the output based on 7 "nearest" examples
        # clf.fit(X_train, y_train)

        # y_pred = clf.predict(X_test)

        # _ = pd.DataFrame({'y_true': y_test, 'y_pred': y_pred}).plot(figsize=(15, 2), alpha=.7)
        # print('Classification accuracy: ', np.mean(y_test == y_pred))

        # %%time

        from backtesting import Backtest, Strategy

        # N_TRAIN = 900
        N_TRAIN = round(len(df)*0.5) ## use 30% of data to train


        class MLTrainOnceStrategy(Strategy):
            price_delta = .04  # 004 = 0.4%

            def init(self):        
                # Init our model, a kNN classifier
                self.clf = KNeighborsClassifier(20)

                # Train the classifier in advance on the first N_TRAIN examples
                df = self.data.df.iloc[:N_TRAIN]
                X, y = get_clean_Xy(df)
                self.clf.fit(X, y)

                # Plot y for inspection
                self.I(get_y, self.data.df, name='y_true')

                # Prepare empty, all-NaN forecast indicator
                self.forecasts = self.I(lambda: np.repeat(np.nan, len(self.data)), name='forecast')

            def next(self):
                # Skip the training, in-sample data
                if len(self.data) < N_TRAIN:
                    return

                # Proceed only with out-of-sample data. Prepare some variables
                high, low, close = self.data.High, self.data.Low, self.data.Close
                current_time = self.data.index[-1]

                # Forecast the next movement
                X = get_X(self.data.df.iloc[-1:])
                forecast = self.clf.predict(X)[0]

                # Update the plotted "forecast" indicator
                self.forecasts[-1] = forecast

                # If our forecast is upwards and we don't already hold a long position
                # place a long order for 20% of available account equity. Vice versa for short.
                # Also set target take-profit and stop-loss prices to be one price_delta
                # away from the current closing price.
                upper, lower = close[-1] * (1 + np.r_[1, -1]*self.price_delta)

                if forecast == 1 and not self.position.is_long:
                    self.buy(size=.2, tp=upper, sl=lower)
                elif forecast == -1 and not self.position.is_short:
                    self.sell(size=.2, tp=lower, sl=upper)

                # Additionally, set aggressive stop-loss on trades that have been open 
                # for more than two days
                for trade in self.trades:
                    if current_time - trade.entry_time > pd.Timedelta('2 days'):
                        if trade.is_long:
                            trade.sl = max(trade.sl, low)
                        else:
                            trade.sl = min(trade.sl, high)
                

        bt = Backtest(data, MLTrainOnceStrategy, commission=.0002, margin=.05)
        return bt