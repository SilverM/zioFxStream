### Credentials
from polygon import RESTClient
from typing import cast
from urllib3 import HTTPResponse
api_key = <apikey>
client = RESTClient(api_key = api_key)
# aggs = client.get_aggs("AAPL", 1, "minute", "2022-04-04", "2022-04-04")

aggs = cast(
    HTTPResponse,
    client.get_aggs(
        "C:EURUSD",
        1,
        "day",
        "2011-01-01",
        "2022-04-20",
        raw=True,
    ),
)


import json
data = json.loads(aggs.data)

import pandas as pd
import datetime

def conversion(x):
    return datetime.datetime.fromtimestamp(x / 1e3)


# api-endpoint
URL = "https://api.polygon.io/v2/aggs/ticker/C:EURUSD/range/1/minute/2021-04-22/2022-04-22?adjusted=true&sort=asc&limit=50000&apiKey=3ctpdsqVwckSoHTDTlv4mB9drztufFjv"
  
# sending get request and saving the response as response object
r = requests.get(url = URL)
  
# extracting data in json format
data = r.json()  

import pandas as pd
eurusd = pd.DataFrame(data['results'])
eurusd.head()

import datetime

def conversion(x):
    return datetime.datetime.fromtimestamp(x / 1e3)


## Request period of data

# importing the requests library
import requests
from polygon import RESTClient
from typing import cast
from urllib3 import HTTPResponse
import pandas as pd

import requests
import time

import datetime

def conversion(x):
    return datetime.datetime.fromtimestamp(x / 1e3)
usdcad['t']  = usdcad['t'].apply(conversion)
usdcad['olag1']= usdcad['c'].shift(1)
usdcad['returns'] = (usdcad['olag1'] - usdcad['c']) / usdcad['olag1']

usdcad.shape

def datetime_to_date(x):
    return x.date()
usdcad['datestr']  = usdcad['t'].apply(datetime_to_date)

## Postgres data inputs
from sqlalchemy import create_engine
engine = create_engine('postgresql://<localhost>/Polygon-io-data')
eurusd.to_sql('xrpbtc_2012_2022', engine)

## Full extract for multiple currencies

url_list = []
for i,v in zip(end_date_list,start_dates_list):
    s = str(i.date())
    e = str(v.date())
    curr = 'X:XRPBTC'
    URL = "https://api.polygon.io/v2/aggs/ticker/{}/range/1/minute/{}/{}?adjusted=true&sort=asc&limit=50000&apiKey={}".format(curr,s,e,api_key)
    url_list.append(URL)

all_tickers = 'https://api.polygon.io/v2/snapshot/locale/global/markets/crypto/tickers?apiKey=3ctpdsqVwckSoHTDTlv4mB9drztufFjv'
forex_tickers = 'https://api.polygon.io/v2/snapshot/locale/global/markets/forex/tickers?apiKey=3ctpdsqVwckSoHTDTlv4mB9drztufFjv'
r = requests.get(url = all_tickers)
data = r.json()  

list2 = []
for i in range(len(data['tickers'])):
    list2.append(data['tickers'][i]['ticker'])

import datetime
from polygon import RESTClient
from typing import cast
from urllib3 import HTTPResponse
import requests
from polygon import RESTClient
from typing import cast
from urllib3 import HTTPResponse
import pandas as pd

def conversion(x):
    return datetime.datetime.fromtimestamp(x / 1e3)

api_key = <api keys>
client = RESTClient(api_key = api_key)

start_date = pd.to_datetime('2012-01-01')
start_dates_list = [start_date]
end_date_list = []

days_interval = 30
while start_date < pd.to_datetime('2022-07-01'):
    start_date = start_date +  pd.to_timedelta(days_interval, unit = 'D')
    start_dates_list.append(start_date)
    
for i in start_dates_list:
    end_date_list.append(i + pd.to_timedelta(1, unit = 'D'))

start_dates_list.pop(0)
freq = ['minute']

for x in freq:
    for a in list2: 
        curr = str(a)
        globals()[a[2:]] = pd.DataFrame()

        for i,v in zip(end_date_list,start_dates_list):
            s = str(i.date())
            e = str(v.date())
            print(curr)
            URL = "https://api.polygon.io/v2/aggs/ticker/{}/range/1/{}/{}/{}?adjusted=true&sort=asc&limit=50000&apiKey={}".format(curr,x,s,e,api_key)
            print(URL)
            # url_list.append(URL)
            r = requests.get(url = URL)
            print(r)
            data = r.json()  
            if data['resultsCount'] == 0:
                pass
            else:
                globals()[a[2:]] = globals()[a[2:]].append(data['results'])
                

        globals()[a[2:]]['t']  = globals()[a[2:]]['t'].apply(conversion)
        globals()[a[2:]]['olag1']= globals()[a[2:]]['c'].shift(1)
        globals()[a[2:]]['returns'] = (globals()[a[2:]]['olag1'] - globals()[a[2:]]['c']) / globals()[a[2:]]['olag1']
        globals()[a[2:]]['currency'] = a[2:]
        path='/Volumes/SeagateExpansion/dataForex/'
        globals()[a[2:]].to_csv(path+'{}_{}.csv'.format(a[2:], x))
print(curr +"completed")