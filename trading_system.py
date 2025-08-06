from data_loader import load_data, compute_log_returns
from hmm_model import hmm_model, label_regimes
from regime_strategy import apply_regime_strategy
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np 

def visualize_market_regimes(df, regime_labels):
	plt.figure(figsize=(15,6))
	colors = {'bull': 'green', 'bear': 'red'}

	for regime in ['bull', 'bear']:
		subset = df[df['regime_'] == regime]
		plt.plot(subset.index, subset['Close_SPY'], color=colors[regime], label=regime)

	plt.title("Market Regimes")
	plt.xlabel("Date")
	plt.ylabel("SPY Price")
	plt.legend()
	plt.tight_layout()
	plt.grid(True)
	plt.show()

def main():
	df = load_data()
	df['Log Returns'] = compute_log_returns(df)
	df.dropna(inplace=True)
	log_returns = np.array(df['Log Returns'].tolist())
	model,hidden_states = hmm_model(log_returns)

	df_regimes, regime_labels, state_series = label_regimes(df, log_returns, hidden_states)

	df['state'] = hidden_states
	df['regime'] = df['state'].map(regime_labels)
	df.columns = ['_'.join(col).strip() if isinstance(col, tuple) else col for col in df.columns]
	print(df.columns)
	df_with_signals = apply_regime_strategy(df)
	print(df_with_signals[['Close_SPY', 'regime_', 'signal']].tail(10))
	visualize_market_regimes(df,regime_labels)

if __name__ == "__main__":
	main()