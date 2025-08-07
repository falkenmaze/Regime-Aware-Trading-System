import pandas as pd 
import matplotlib.pyplot as plt 
def backtest(df, initial_cash= 100000, risk_per_trade_pct=0.01, stop_loss_pct=0.1, sell_pct=0.3):
	df = df.copy()
	df['position'] = 0 # current position: 1 if holding, 0 if not
	df['shares'] = 0
	df['cash'] = float(initial_cash)
	df['portfolio_value'] = float(initial_cash)
	df['entry_price'] = None
	holding = False
	entry_price = None # Price at which current position was entered

	for i in range(1, len(df)):
		today = df.index[i]
		prev = df.index[i-1]

		# carry forward previous values
		df.at[today, 'position'] = df.at[prev, 'position']
		df.at[today, 'shares'] = df.at[prev, 'shares']
		df.at[today, 'cash'] = df.at[prev, 'cash']
		if df.at[today, 'position'] == 0:
			entry_price = None
		df.at[today, 'entry_price'] = entry_price

		price = float(df.at[today, 'Close_SPY'])

		# Execute trades based on signal
		if df.at[today, 'signal'] == 1 and df.at[prev, 'position'] == 0:
			# Buy
			max_buy_pct = 0.25
			max_risk = risk_per_trade_pct * df.at[prev, 'portfolio_value']
			risk_per_share = stop_loss_pct * price
			if risk_per_share > 0:
				buy_cash = df.at[today, 'cash'] * max_buy_pct
				shares_by_cash = int((df.at[today, 'cash'] * max_buy_pct) // price)
				shares_by_risk = int(max_risk // risk_per_share)
				shares_to_buy = min(shares_by_cash, shares_by_risk)
				cost = shares_to_buy * price
				if shares_to_buy > 0 and cost <= df.at[today, 'cash']:
					df.at[today, 'shares'] += shares_to_buy
					df.at[today, 'position'] = 1
					df.at[today, 'cash'] -= cost 
					entry_price = price
					df.at[today, 'entry_price'] = price

		if df.at[today, 'position'] > 0 and entry_price is not None:
			if price <= entry_price * (1 - stop_loss_pct):
				proceeds = df.at[today, 'shares'] * price 
				df.at[today, 'cash'] += proceeds 
				df.at[today, 'position'] = 0
				df.at[today, 'shares'] = 0
				entry_price = None

		elif df.at[today, 'signal'] == -1 and df.at[prev, 'shares'] > 0:
			# Sell
			shares_to_sell = int(df.at[prev, 'shares'] * sell_pct)
			proceeds = shares_to_sell * price
			if shares_to_sell > 0:
				df.at[today, 'cash'] += proceeds
				df.at[today, 'shares'] = df.at[prev, 'shares'] - shares_to_sell
				# keep position 1 if shares remain
				if df.at[today, 'shares'] == 0:
					df.at[today, 'position'] = 0

		# Portfolio value = cash + current position * price
		df.at[today, 'portfolio_value'] = (
			df.at[today, 'cash'] + df.at[today, 'shares'] * df.at[today, 'Close_SPY']
			)
	return df

def plot_backtest_results(df):
	plt.figure(figsize=(12,6))
	plt.plot(df.index, df['portfolio_value'], label='Portfolio Value')
	plt.title("Backtest Results")
	plt.xlabel("Date")
	plt.ylabel("Portfolio Value ($)")
	plt.legend()
	plt.grid(True)
	plt.tight_layout()
	plt.show()