from data_loader import load_data, compute_log_returns

df = load_data()
df['Log Returns'] = compute_log_returns(df)
df.dropna(inplace=True)
print(df.head())