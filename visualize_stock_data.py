
# Run this AFTER stock_data_pipeline.py has already loaded data into the StockPrices table

import pandas as pd
import numpy as np
import pyodbc
import matplotlib.pyplot as plt

TICKERS = ["AAPL", "NVDA", "META"]

# ---- Pull everything from SQL ----
connection = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};"
    "SERVER=.\\SQLEXPRESS;"
    "DATABASE=FinancialData;"
    "Trusted_Connection=yes;"
    "TrustServerCertificate=yes;"
)

query = """
    SELECT TradeDate, Ticker, ClosePrice, daily_return
    FROM [FinancialData].[dbo].[StockPrices]
    ORDER BY TradeDate
"""
data = pd.read_sql(query, connection)
connection.close()

data["TradeDate"] = pd.to_datetime(data["TradeDate"])

# pivot so each ticker becomes its own column, indexed by date
closes = data.pivot(index="TradeDate", columns="Ticker", values="ClosePrice")
returns = data.pivot(index="TradeDate", columns="Ticker",
                     values="daily_return")

closes = closes[TICKERS]
returns = returns[TICKERS]

# Chart 1: normalized price
# divide each column by its own first value, times 100. now every ticker "starts" at 100 no matter its actual dollar price.
normalized = closes / closes.iloc[0] * 100

"""Compare Table of Closes of AAPL, NVDA, META over the last 8 years (96 months)"""
fig, ax = plt.subplots(figsize=(10, 5))
for ticker in TICKERS:
    ax.plot(normalized.index, normalized[ticker], label=ticker, linewidth=1.5)
ax.axhline(100, color="gray", linewidth=0.8, linestyle="--")
ax.set_title("Normalized Price (Base = 100)")
ax.set_xlabel("Date")
ax.set_ylabel("Indexed Price")
ax.legend()
ax.grid(alpha=0.3)
fig.tight_layout()
fig.savefig("normalized_price.png", dpi=150)


# Chart 2: cumulative return

daily_decimal = returns.fillna(0) / 100
cumulative_return = (1 + daily_decimal).cumprod() * 100 - 100

"""Compare Cumulative Return of AAPL, NVDA, META over the last 8 years (96 months)"""

fig, ax = plt.subplots(figsize=(10, 5))
for ticker in TICKERS:
    ax.plot(cumulative_return.index,
            cumulative_return[ticker], label=ticker, linewidth=1.5)
ax.axhline(0, color="gray", linewidth=0.8, linestyle="--")
ax.set_title("Cumulative Return (%)")
ax.set_xlabel("Date")
ax.set_ylabel("Total Return (%)")
ax.legend()
ax.grid(alpha=0.3)
fig.tight_layout()
fig.savefig("cumulative_return.png", dpi=150)

# Chart 3: risk / return scatter
annualized_return = returns.mean() * 252
annualized_vol = returns.std() * np.sqrt(252)
sharpe = annualized_return / annualized_vol

fig, ax = plt.subplots(figsize=(7, 6))
sizes = (sharpe - sharpe.min() + 0.5) * 400

scatter = ax.scatter(
    annualized_vol, annualized_return, s=sizes, c=sharpe,
    cmap="viridis", edgecolor="black", linewidth=0.8
)

for ticker in TICKERS:
    ax.annotate(
        ticker, (annualized_vol[ticker], annualized_return[ticker]),
        textcoords="offset points", xytext=(8, 8), fontsize=10
    )

ax.set_title("Risk vs Return (annualized)")
ax.set_xlabel("Annualized Volatility (%)")
ax.set_ylabel("Annualized Return (%)")
ax.grid(alpha=0.3)
cbar = fig.colorbar(scatter, ax=ax)
cbar.set_label("Sharpe Ratio")
fig.tight_layout()
fig.savefig("risk_return_scatter.png", dpi=150)

plt.show()

print("Saved: normalized_price.png, cumulative_return.png, risk_return_scatter.png")
