from hmmlearn.hmm import GaussianHMM
import numpy as np 
import pandas as pd 

def hmm_model(log_returns, n_components=2):
	if len(log_returns.shape) == 1:
		log_returns = log_returns.reshape(-1,1)
	model = GaussianHMM(n_components = 2, covariance_type='full')
	model.fit(log_returns)
	hidden_states = model.predict(log_returns)
	return model, hidden_states

def label_regimes(df, log_returns, hidden_states):
	df = pd.DataFrame({
		'return': log_returns.flatten(),
		'state': hidden_states
		})
	
	regime_stats = df.groupby('state')['return'].agg(['mean', 'std'])

	sorted_states = regime_stats.sort_values('mean').index.tolist()

	regime_labels = {
	sorted_states[0]: 'bear',
	sorted_states[1]: 'bull'
	}

	state_series = df['state'].map(regime_labels)

	return df, regime_labels, state_series