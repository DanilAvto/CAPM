# loading libraries
import numpy as np
import pandas as pd
from pandas_datareader import data as web
import yfinance as yfin
from dateutil.relativedelta import relativedelta
from datetime import date
today = date.today()
yfin.pdr_override()
# portfolio of stocks parsing
tickers = ['MSFT', 'PEP', 'ACN', 'C', 'META','OMV.VI', 'UBSG.SW', 'ZURN.SW', 'BMW.DE', '6758.T', '^GSPC']
#loading into a new DF
portfolio = pd.DataFrame()
for ticker in tickers:
    portfolio[ticker] = web.get_data_yahoo(ticker,start = '2018-10-20', end = '2023-10-20')['Adj Close']
# changing column names
column_names = ['Microsoft', 'Pepsico', 'Accenture', 'Citigroup', 'Meta', 'OMV', 'UBS', 'Zurich_Insurance_Group', 'BMW', 'Sony', 'S&P500']
portfolio.columns = column_names
#print(portfolio.head(5))
# checking the length of a DF
#print(len(portfolio))
# checking null values
#print(portfolio.isna().sum())
# finding companies with missing data
missing_values = portfolio.isna().sum() > 0
comp_miss_val = portfolio.columns[missing_values]
for i in comp_miss_val:
    portfolio[i] = portfolio[i].fillna(method='ffill')
# no missing data anymore
#print(portfolio.isna().sum())
for i in comp_miss_val:
    portfolio[i] = portfolio[i].fillna(method='bfill')
#print(portfolio.isna().sum())
# finding returns of stocks
returns = np.log(portfolio/portfolio.shift(1))
#print(returns)

# building a covariance matrix
covariance_matrix = returns.cov() * 252
#print(covariance_matrix)
# finding market variance (S&P 500)
market_variance = returns['S&P500'].var() * 252
#print(market_variance)
# storing covariances for each stock with S&P 500
covariance = {}
for key, value in covariance_matrix.items():
    cov = covariance_matrix.loc[key]['S&P500']
    covariance[key] = cov
#print(covariance)
# getting rid of S&P variance bcs we have it under the name market_variance already
covariance.pop('S&P500')
#print(covariance)

# calculating betas for each stock in the portfolio
betas = {}
for key, value in covariance.items():
    beta = covariance[key] / market_variance
    betas[key] = beta
#print(betas)
# CAPM = risk free rate + beta * (market return - risk free rate)
# for risk free rate we gonna use 10 years Treasury bills USA
risk_free_rate = 0.0498
# calculating a market return ove the last 5 years (avg.annual)
market_return = (portfolio['S&P500'].iloc[-1] / portfolio['S&P500'].iloc[0] - 1) / 5
#print(market_return)
# Equity risk premium calculations
erp = market_return - risk_free_rate
#print(erp)

#finding CAPM returns for each stock

CAPM_returns = {}
for key, value in betas.items():
    capm_return = risk_free_rate + value * erp
    capm_return = round(capm_return * 100,2)
    CAPM_returns[key] = capm_return
#print(CAPM_returns)
# printing CAPM returns for each stock
for key,value in CAPM_returns.items():
    print(f'CAPM return of a stock {key} equals to {value} %')


