import numpy as np 
import pandas as pd 

def compute_metrics(df):
	df = df.copy()
	df = df[df['portfolio_value'] > 0] 

	# Daily Returns
	df['daily_return'] = df['portfolio_value'].pct_change()

	total_return = df['portfolio_value'].iloc[-1] / df['portfolio_value'].iloc[0] - 1

	# CAGR
	days = (df.index[-1] - df.index[0]).days 
	cagr = (df['portfolio_value'].iloc[-1] / df['portfolio_value'].iloc[0]) ** (365/days) - 1 

	# Sharpe Ratio (assuming risk-free rate = 0)
	returns = df['portfolio_value'].pct_change().dropna()
	sharpe = returns.mean() / returns.std() * np.sqrt(252)

	# Max Drawdown
	cum_max = df['portfolio_value'].cummax()
	drawdown = df['portfolio_value'] / cum_max - 1
	max_drawdown = drawdown.min()

	# Trade Metrics
	trades = df[df['signal'].diff() != 0] # trades happen where signal changes
	num_trades = len(trades)

	returns = df['portfolio_value'].pct_change().fillna(0)
	avg_trade_return = returns[trades.index].mean() if num_trades > 0 else 0

	# Win Rate
	trade_returns = returns[trades.index]
	win_rate = (trade_returns > 0).mean() if num_trades > 0 else 0 

	# Trade Duration
	holding_days = df['position'].diff().fillna(0)
	enter_days = df[holding_days == 1].index
	exit_days = df[holding_days == -1].index 
	durations = [(exit - enter).days for enter,exit in zip(enter_days, exit_days)]
	avg_duration = np.mean(durations) if durations else 0

	return {
	"Total Return": f"{total_return:.2%}",
	"CAGR": f"{cagr:.2%}",
	"Sharpe Ratio": f"{sharpe:.2%}",
	"Max Drawdown": f"{max_drawdown:.2%}",
	"Win Rate": f"{win_rate:.2%}",
	"Avg Trade Return": f"{avg_trade_return:.2%}",
	"Number of Trades": num_trades,
	"Avg Trade duration": f"{avg_duration:.1f} days"
	}