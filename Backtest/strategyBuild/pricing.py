import pandas as pd
from bokeh.models import Band, ColumnDataSource
from bokeh.layouts import row, column
from bokeh.models import CustomJS
from bokeh.models import NumeralTickFormatter
from bokeh.models.widgets import Select
from bokeh.plotting import figure, ColumnDataSource, show
from bokeh.transform import stack
from bokeh.models import CustomJS, ColumnDataSource, Select, Column
from bokeh.plotting import figure, show
from bokeh.models import NumeralTickFormatter
import numpy as np
from backtesting import Backtest, Strategy

import pandas as pd

class Pricing():
    def __init__(self):
        pass

    def run():
        ##ETHAUD
        df = pd.read_csv("/Users/leqisoon/Documents/Coding/RegimeD/eurusd.csv")
        # df = pd.read_csv("../eurusd.csv")
        df.head()

        start_date = '2011-01-01'
        end_date = '2022-06-30'
        mask = (df['t'] > start_date) & (df['t'] <= end_date)
        df = df.loc[mask]


        df['Open'] = df['o'] 
        df['High'] = df['h'] 
        df['Low'] = df['l'] 
        df['Close'] = df['c'] 
        df['Volume'] = df['v'] 

        df2 = df[['Open','High','Low', 'Close', 'Volume']]
        df2.index = pd.to_datetime((df['t']))

        ##BTCUSD
        # df_ethbtc = pd.read_csv("/Volumes/SeagateExpansion/dataForex_trades/USDGBP_day.csv")
        df_ethbtc = pd.read_csv("/Users/leqisoon/Documents/Coding/RegimeD/eurusd.csv")
        df_ethbtc.head()

        start_date = '2015-01-01'
        end_date = '2022-04-30'
        mask = (df_ethbtc['t'] > start_date) & (df_ethbtc['t'] <= end_date)
        df_ethbtc = df_ethbtc.loc[mask]

        df_ethbtc.shape

        df_ethbtc['Open'] = df_ethbtc['o'] 
        df_ethbtc['High'] = df_ethbtc['h'] 
        df_ethbtc['Low'] = df_ethbtc['l'] 
        df_ethbtc['Close'] = df_ethbtc['c'] 
        df_ethbtc['Volume'] = df_ethbtc['v'] 

        df2_ethbtc = df_ethbtc[['Open','High','Low', 'Close', 'Volume']]
        df2_ethbtc.index = pd.to_datetime((df_ethbtc['t']))
        
        
        x = df2.index
        y = df2.Close

        df_test = pd.DataFrame(data=dict(x=x, y=y)).sort_values(by="x")

        sem = lambda x: x.std() / np.sqrt(x.size)
        df2_test = df_test.y.rolling(window=20).agg({"y_mean": np.mean, "y_std": np.std, "y_sem": sem})
        df2_test = df2_test.fillna(method='bfill')

        df_test = pd.concat([df_test, df2_test], axis=1)
        df_test['lower'] = df_test.y_mean - 2*df_test.y_std
        df_test['upper'] = df_test.y_mean + 2*df_test.y_std

        x = df2_ethbtc.index
        y = df2_ethbtc.Close

        df_test2 = pd.DataFrame(data=dict(x=x, y=y)).sort_values(by="x")

        sem = lambda x: x.std() / np.sqrt(x.size)
        df2_test2 = df_test2.y.rolling(window=20).agg({"y_mean": np.mean, "y_std": np.std, "y_sem": sem})
        df2_test2 = df2_test2.fillna(method='bfill')

        df_test2 = pd.concat([df_test2, df2_test2], axis=1)
        df_test2['lower'] = df_test2.y_mean - 2*df_test2.y_std
        df_test2['upper'] = df_test2.y_mean + 2*df_test2.y_std

        

        
        myPlot = figure(x_axis_type='datetime'
                        , width=1400
            # y_range = (0, 4)
        )

        data =  {'EURUSD': {'x': df2.index, 'y': df2.Close, 'lower': df_test['lower'], 'upper':df_test['upper']},
                 'USDGBP': {'x': df2_ethbtc.index, 'y':df2_ethbtc.Close, 'lower': df_test2['lower'], 'upper':df_test2['upper']}
                }

        source = ColumnDataSource(data['EURUSD'])
        myPlot.line('x', 'y', line_width = 2, source = source)
        band = Band(base='x', lower='lower', upper='upper', source=source, level='underlay',
                    fill_alpha=1.0, line_width=1, line_color='black')
        myPlot.add_layout(band)

        callback = CustomJS(args = {'source': source, 'data': data},
        code = """source.data = data[cb_obj.value]; """)

        select = Select(title = 'Choose', value = 'EURUSD', options = ['EURUSD', 'USDGBP'])
        select.js_on_change('value', callback)

        myPlot.title.text = "Rolling Standard Deviation"
        myPlot.xgrid[0].grid_line_color=None
        myPlot.ygrid[0].grid_line_alpha=0.5
        myPlot.xaxis.axis_label = 'Date'
        myPlot.yaxis.axis_label = 'Price'
        myPlot.yaxis[0].formatter = NumeralTickFormatter(format="0.00")

        
        
        
        layout = Column(select, myPlot)
        return layout
