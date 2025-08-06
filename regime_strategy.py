import pandas as pd 

def bull_strategy(df):
	"""
	Bull Regime: Trend Following Strategy (Buy if Close_SPY > MA50)
	"""
	df = df.copy()
	df['ma50'] = df['Close_SPY'].rolling(window=50).mean()
	df['signal'] = 0 # Buy = 1; Hold = 0; Sell = -1
	df.loc[df['Close_SPY'] > df['ma50'], 'signal'] = 1
	df.loc[df['Close_SPY'] < df['ma50'], 'signal'] = -1
	return df[['signal']].reindex(df.index)

def bear_strategy(df):
	"""
	Bear Regime: Mean-reversion strategy (Buy if Close_SPY < lower bollinger band)

	"""
	df = df.copy()
	df['ma20'] = df['Close_SPY'].rolling(window=20).mean()
	df['std20'] = df['Close_SPY'].rolling(window=20).std()
	df['lower_bb'] = df['ma20'] - 2 * df['std20']
	df['signal'] = 0 
	df.loc[df['Close_SPY'] < df['lower_bb'], 'signal'] = 1 
	df.loc[df['Close_SPY'] > df['lower_bb'], 'signal'] = -1
	return df[['signal']].reindex(df.index)


def apply_regime_strategy(df):
	"""
	Applies the correct strategy depending on the regime (bull/bear)

	"""
	df = df.copy()
	df['signal'] = 0 #default

	bull_df = df[df['regime_'] == 'bull']
	bear_df = df[df['regime_'] == 'bear']

	df.update(bull_strategy(bull_df))
	df.update(bear_strategy(bear_df))

	return df 