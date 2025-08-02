# Download SPY historical prices using yfinance, prepare a clean Dataframe and engineer features
import yfinance as yf
import pandas as pd
import numpy as np

def load_data(ticker='SPY', start='2000-01-01', end='2024-01-01'):
	df = yf.download(ticker, start=start, end=end)
	df = df[['Close']]
	return df

def compute_log_returns(df: pd.DataFrame) -> pd.Series:
	return np.log(df['Close'] / df['Close'].shift(1)).dropna()
