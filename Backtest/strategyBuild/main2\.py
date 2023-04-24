from backtesting import Backtest, Strategy
from pricing import Pricing
from KNN import Knnpredictor_2020_after
from KNN_2020 import Knnpredictor_2020_before
from SMACross import Crosscurrency
from strategy import Tabview

import pandas as pd
# df = pd.read_csv("/Volumes/SeagateExpansion/dataForex_trades/CADUSD_minute.csv")
df = pd.read_csv("/Volumes/SeagateExpansion/dataForex/ETHUSD_day.csv")

df.head()

start_date = '2018-07-01'
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



# ### adding stats chart
from bokeh.models import ColumnDataSource, TableColumn, DataTable, HTMLTemplateFormatter
from bokeh.io import show
from bokeh.resources import INLINE

y = []
for i in list(stats[:27].to_dict().values()):
    y.append(str(i))

data = {'x_values': list(stats[:27].to_dict().keys()),
        'y_values': y}

columns = [
        TableColumn(field="x_values", title="Metric"),
        TableColumn(field="y_values", title="Results"),
    ]


stats2, s3_v2 = Crosscurrency.run_()



source = ColumnDataSource(data=data)
data_table = DataTable(source=source, 
                       columns=columns, width=400, height=800)

zn = []
for i in list(stats2[:27].to_dict().values()):
    zn.append(str(i))

data4 = {'x_values': list(stats2[:27].to_dict().keys()),
        'y_values': zn}

columns = [
        TableColumn(field="x_values", title="Metric"),
        TableColumn(field="y_values", title="Results"),
    ]

source4 = ColumnDataSource(data=data4)
data_table4 = DataTable(source=source4, 
                       columns=columns, width=400, height=800)
# myapp.py

from random import random
from bokeh.layouts import row
from bokeh.layouts import column
from bokeh.models import Button
from bokeh.palettes import RdYlBu3
from bokeh.plotting import figure, curdoc
from bokeh.models.widgets import Panel, Tabs
from bokeh.models import ColumnDataSource

    
knn_results = Knnpredictor_2020_after.run()
# knn_results.run()
z = []
for i in list(knn_results.run().to_dict().values()):
    z.append(str(i))


data2 = {'x_values': list(knn_results.run()[:27].to_dict().keys()),
        'y_values': z}

columns = [
        TableColumn(field="x_values", title="Metric"),
        TableColumn(field="y_values", title="Results"),
    ]
source2 = ColumnDataSource(data=data2)
data_table2 = DataTable(source=source2, 
                       columns=columns, width=400, height=800)

knn_results2 = Tabview.run()

def update():
    from strategy import Tabview
    global knn_results2
    knn_results2 = Tabview.run()


# knn_results2= update()
# knn_results.run()
a = []
for i in list(knn_results2.run().to_dict().values()):
    a.append(str(i))


data3 = {'x_values': list(knn_results2.run()[:27].to_dict().keys()),
        'y_values': a}

columns = [
        TableColumn(field="x_values", title="Metric"),
        TableColumn(field="y_values", title="Results"),
    ]
source3 = ColumnDataSource(data=data3)
data_table3 = DataTable(source=source3, 
                       columns=columns, width=400, height=800)

# add a button widget and configure with the call back


tab1 = Panel(child = Pricing.run(), title = 'Currency Historicals') # historicals
tab2 = Panel(child=row(s3,data_table), title="ETHUSD - SMA Crossover") 
tab5 = Panel(child=row(s3_v2,data_table4), title="CADUSD_day - SMA Crossover") # sma plot

tab3 = Panel(child = row(knn_results.plot(), data_table2), title = 'EURUSD_day - KNN') #after 2020 knn
# tab4 = Panel(child = row(knn_results2.plot(), data_table3), title = 'USDGBP_day - KNN')
tab4 = Panel(child = row(knn_results2.plot(), data_table3), title = 'Custom metric')

tabs = Tabs(tabs=[ tab1, tab5, tab2, tab3, tab4 ])

# put the button and plot in a layout and add to the document
# curdoc().add_root(column(button, p,s3))
curdoc().add_root(tabs)
# curdoc().add_periodic_callback(callback, 100)
curdoc().add_periodic_callback(update, 1000)