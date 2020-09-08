import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.linear_model import LinearRegression
import pandas_datareader.data as web
import investpy as inv
import yfinance as yf
import pyfolio as pf
import warnings

yf.pdr_override()
warnings.filterwarnings('ignore')


tickers = ['PETR4.SA', 'ENAT3.SA', 'VALE3.SA']
dados_yahoo = web.get_data_yahoo(tickers, period='5y')['Adj Close']
petrobras = dados_yahoo['PETR4.SA'].reset_index()
enauta = dados_yahoo['ENAT3.SA'].reset_index()
vale = dados_yahoo['VALE3.SA'].reset_index()

petroleo = web.get_data_yahoo(['BZ=F'], period='5y').reset_index()
ibov = web.get_data_yahoo(['^BVSP'], period='5y').reset_index()

petrobras1 = petrobras[petrobras['Date'] > '2020-01-03']
enauta1 = enauta[enauta['Date'] > '2020-01-03']
vale1 = vale[vale['Date'] > '2020-01-03']
ibov1 = ibov[ibov['Date'] > '2020-01-03']
df = petroleo.merge(petrobras1).merge(enauta1).merge(vale1)

###############################
df = df.fillna(df.mean())
X = df[['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']]
Y = df['PETR4.SA']
reg = LinearRegression().fit(X, Y)
reg.score(X,Y)

today = petroleo.iloc[-1][['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']].values.reshape(1,-1)
print(reg.predict(today))
###############################

df['Close'] = df['Close']/df['Close'].iloc[0]
df['PETR4.SA'] = df['PETR4.SA']/df['PETR4.SA'].iloc[0]
df['ENAT3.SA'] = df['ENAT3.SA']/df['ENAT3.SA'].iloc[0]
df['VALE3.SA'] = df['VALE3.SA']/df['VALE3.SA'].iloc[0]
#df.plot('Date', ['Close', 'PETR4.SA'])
ibov1['Close'] = ibov1['Close']/ibov1['Close'].iloc[0]

plt.plot(df['Date'], df['PETR4.SA'])
plt.plot(df['Date'], df['ENAT3.SA'])
plt.plot(df['Date'], df['VALE3.SA'])
plt.plot(df['Date'], df['Close'])
plt.plot(ibov1['Date'], ibov1['Close'])
plt.legend(['PETR4', 'ENAT3', 'VALE3', 'Brent', 'IBOV'])