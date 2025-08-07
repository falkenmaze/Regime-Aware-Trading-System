# Regime Aware Trading System
This project implements a **regime-aware trading system** that adapts its strategy based on market regimes. It uses macroeconomic and price-based indicators to detect regimes like bull and bear, then applies tailored strategies within each regime. The system is backtested using historical SPY data, with risk controls such as stop-losses and position sizing in place.

---

## 📈 Strategy Used 

### 1. **Regime Detection**
- Utilizes a **Hidden Markov Model** to detect different market regimes.
- Regimes are labeled as `bull` or `bear` based on model state and return characteristics.
- <img width="1866" height="752" alt="image" src="https://github.com/user-attachments/assets/7df14861-c530-4dd2-a143-21f1d52886ff" />


### 2. **Regime-Specific Trading**
- **Bull Regime**: Trend-following strategy using moving average crossover or momentum.
- **Bear Regime**: Defensive strategy based on moving average and bollinger bands crossover.

---

## Backtesting Engine

- **Capital**: `$100,000` starting capital.
- **Trade Sizing**: Fixed percentage of capital (e.g., 25%) with a **1% risk cap** per trade.
- **Partial Exits**: Sells a configurable percentage (e.g., 30%) on each sell signal.
- **Stop Loss**: Dynamic stop-loss applied per trade (default: 10%).
- **Performance Tracking**: Portfolio value, trades, durations, and more.

---

## 📊 Performance Metrics

| Metric                | Value        |
|-----------------------|--------------|
| **Total Return**      | 63.34%       |
| **CAGR**              | 2.07%        |
| **Sharpe Ratio**      | 47.42        |
| **Max Drawdown**      | -12.95%      |
| **Win Rate**          | 49.03%       |
| **Avg Trade Return**  | -0.01%       |
| **# of Trades**       | 1911         |
| **Avg Trade Duration**| 113.8 days   |

---

## 📸 Results and Visuals

### 🔹 Portfolio Value Over Time
> _Backtest result over full date range._
<img width="1497" height="755" alt="image" src="https://github.com/user-attachments/assets/53e2cb80-0b92-4ed1-a44b-c3d87c11b7ac" />

---

---

## 🚀 How to Run

### 1. Clone the Repository
```bash
git clone https://github.com/<your-username>/regime-aware-trading-system.git
cd regime-aware-trading-system
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run Backtest
```bash
python trading_system.py
```
