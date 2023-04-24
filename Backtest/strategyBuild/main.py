from backtesting import Backtest, Strategy
from pricing import Pricing
from KNN import Knnpredictor_2020_after
from KNN_2020 import Knnpredictor_2020_before
from SMACross import Crosscurrency
from strategy import Tabview
from random import random
from bokeh.layouts import row
from bokeh.layouts import column
from bokeh.models import Button
from bokeh.palettes import RdYlBu3
from bokeh.plotting import figure, curdoc
from bokeh.models.widgets import Panel, Tabs
from bokeh.models import ColumnDataSource

import pandas as pd
df = pd.read_csv("../eurusd.csv")
# df = pd.read_csv("/Volumes/SeagateExpansion/dataForex_trades/USDGBP_day.csv")

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

# ### adding stats chart
from bokeh.models import ColumnDataSource, TableColumn, DataTable, HTMLTemplateFormatter
from bokeh.io import show
from bokeh.resources import INLINE


stats2, s3_v2 = Crosscurrency.run_()

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

### 2

    
knn_results = Knnpredictor_2020_after.run()
# knn_results.run()
z_after = []
for i in list(knn_results.run().to_dict().values()):
    z_after.append(str(i))


data2 = {'x_values': list(knn_results.run()[:27].to_dict().keys()),
        'y_values': z_after}

columns = [
        TableColumn(field="x_values", title="Metric"),
        TableColumn(field="y_values", title="Results"),
    ]
source2 = ColumnDataSource(data=data2)
data_table2 = DataTable(source=source2, 
                       columns=columns, width=400, height=800)



### 2
knn_results_before = Knnpredictor_2020_before.run()
# knn_results.run()
z_before = []
for i in list(knn_results_before.run().to_dict().values()):
    z_before.append(str(i))


data_before = {'x_values': list(knn_results_before.run()[:27].to_dict().keys()),
        'y_values': z_before}

columns = [
        TableColumn(field="x_values", title="Metric"),
        TableColumn(field="y_values", title="Results"),
    ]
source_before = ColumnDataSource(data=data_before)
data_table_before = DataTable(source=source_before, 
                       columns=columns, width=400, height=800)                       


tab1 = Panel(child = Pricing.run(), title = 'Currency Historicals')
tab5 = Panel(child=row(s3_v2,data_table4), title="EURUSD_day - SMA Crossover")
tab3 = Panel(child = row(knn_results.plot(), data_table2), title = 'EURUSD_day - 2020 afterKNN')
tab2 = Panel(child = row(knn_results_before.plot(), data_table_before), title = 'EURUSD_day - 2020 beforeKNN')

# tab4 = Panel(child = row(knn_results2.plot(), data_table3), title = 'USDGBP_day - KNN')

tabs = Tabs(tabs=[ tab1, tab5, tab3, tab2 ])

# put the button and plot in a layout and add to the document
# curdoc().add_root(column(button, p,s3))
curdoc().add_root(tabs)
# curdoc().add_periodic_callback(callback, 100)
# curdoc().add_periodic_callback(update, 1000)