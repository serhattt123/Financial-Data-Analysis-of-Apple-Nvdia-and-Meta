import pandas as pd
import yfinance as yf
import numpy as np

# avoid scientific notation
pd.set_option("display.float_format", "{:.2f}".format)
pd.set_option("display.width", 120)

TICKERS = ["AAPL", "NVDA", "META"]


def section(title):
    print(f"\n{'='*10} {title} {'='*10}")


# ---- Fetch data ----
raw = yf.download(TICKERS, period="96mo", interval="1d", group_by="ticker")

Closes = pd.DataFrame({t: raw[t]["Close"] for t in TICKERS})
Volumes = pd.DataFrame({t: raw[t]["Volume"] for t in TICKERS})

# ---- Data quality checks (only print if something's actually wrong) ----
section("Data Quality")
print("Shape:", Closes.shape)
print("NaN count (Close):\n", Closes.isna().sum())
print("Duplicated dates:", Closes.index.duplicated().sum())
print("First valid date per ticker:\n",
      Closes.apply(lambda s: s.first_valid_index()))
print("Last valid date per ticker:\n",
      Closes.apply(lambda s: s.last_valid_index()))

for t in TICKERS:
    bad_hl = (raw[t]["High"] < raw[t]["Low"]).sum()
    bad_ho = (raw[t]["High"] < raw[t]["Open"]).sum()
    if bad_hl or bad_ho:
        print(f"WARNING: {t} has {bad_hl} High<Low, {bad_ho} High<Open rows")
if (Volumes < 0).any().any():
    print("WARNING: negative volume found")

# ---- Daily return ----
daily_return = Closes.pct_change() * 100
# first row is NaN by definition (no previous day) - expected, not a bug

# ---- Monthly / Yearly return ----


def period_return(close, freq):
    return close.resample(freq).agg(lambda x: (x.iloc[-1] / x.iloc[0] - 1) * 100)


monthly_returns = pd.DataFrame(
    {t: period_return(Closes[t], "ME") for t in TICKERS})
yearly_returns = pd.DataFrame(
    {t: period_return(Closes[t], "YE") for t in TICKERS})

section("Monthly Returns (%) - last 5")
print(monthly_returns.tail())

section("Yearly Returns (%)")
print(yearly_returns)

# ---- Risk & Return summary ----
last_date = daily_return.index.max()
returns_1y = daily_return[daily_return.index >=
                          last_date - pd.DateOffset(years=1)]
returns_8y = daily_return[daily_return.index >=
                          last_date - pd.DateOffset(years=8)]

volatility_1y = returns_1y.std() * np.sqrt(252)
volatility_8y = returns_8y.std() * np.sqrt(252)
annualized_return = daily_return.mean() * 252
sharpe_8y = annualized_return / volatility_8y

# CAGR using each column's own first/last VALID value, not raw iloc[0]/iloc[-1]
start_prices = Closes.apply(lambda s: s.dropna().iloc[0])
end_prices = Closes.apply(lambda s: s.dropna().iloc[-1])
years_span = Closes.apply(lambda s: (
    s.dropna().index[-1] - s.dropna().index[0]).days / 365)
cagr = ((end_prices / start_prices) ** (1 / years_span) - 1) * 100

risk_return = pd.DataFrame({
    "Annualized Return (%)": annualized_return,
    "8Y CAGR (%)": cagr,
    "1Y Volatility (%)": volatility_1y,
    "8Y Volatility (%)": volatility_8y,
    "8Y Sharpe Ratio": sharpe_8y,
}).round(2)

section("Risk & Return Analysis")
print(risk_return)
