# Financial Data Analysis

A Python and SQL Server based financial data analysis project using historical stock market data from Yahoo Finance.

The project focuses on collecting, cleaning, analyzing, and storing financial data while comparing the risk and return characteristics of selected stocks.

## Project Overview

In this project, historical daily stock data is collected using `yfinance` and processed with Python, Pandas, and NumPy.

The processed data is then stored in a local SQL Server database using `pyodbc`. SQL is used to perform additional financial analysis, and the resulting analysis can be retrieved back into Python for further processing and visualization.

### Data Pipeline

```text
Yahoo Finance
      ↓
   yfinance
      ↓
Python / Pandas / NumPy
      ↓
Data Cleaning & Financial Metrics
      ↓
SQL Server
      ↓
SQL Analysis
      ↓
Python
      ↓
Visualization & Reporting
```

## Stocks Analyzed

The current analysis includes:

* Apple (AAPL)
* NVIDIA (NVDA)
* Meta Platforms (META)

Approximately 8 years of daily historical data is analyzed.

## Technologies Used

* Python
* Pandas
* NumPy
* yfinance
* pyodbc
* Microsoft SQL Server
* Matplotlib *(planned for visualization)*
* Seaborn *(planned for visualization)*

## Python Analysis

The Python side of the project currently performs the following analyses:

### Data Collection

Historical daily market data is downloaded from Yahoo Finance using `yfinance`.

The following data is collected:

* Open Price
* High Price
* Low Price
* Close Price
* Trading Volume

### Data Quality Checks

Several checks are performed before analysis, including:

* Missing values
* Duplicated dates
* First and last valid dates
* High/Low price consistency
* High/Open price consistency
* Negative trading volume

### Daily Returns

Daily percentage returns are calculated using:

```python
daily_return = Closes.pct_change() * 100
```

### Monthly and Yearly Returns

Monthly and yearly returns are calculated from the first and last available closing prices within each period.

### Risk & Return Metrics

The following financial metrics are currently calculated:

* Annualized Return
* CAGR (Compound Annual Growth Rate)
* 1-Year Volatility
* 8-Year Volatility
* Sharpe Ratio

### Correlation Analysis

A correlation matrix is calculated using daily returns to examine the relationship between the stocks.

## SQL Server Database

The processed daily stock data is stored in a local Microsoft SQL Server database.

### Database

```text
FinancialData
```

### Main Table

```text
StockPrices
```

The table contains:

| Column       | Description             |
| ------------ | ----------------------- |
| ID           | Unique row identifier   |
| TradeDate    | Trading date            |
| Ticker       | Stock ticker            |
| OpenPrice    | Opening price           |
| HighPrice    | Highest price           |
| LowPrice     | Lowest price            |
| ClosePrice   | Closing price           |
| Volume       | Trading volume          |
| daily_return | Daily percentage return |

Python automatically checks the latest date stored for each ticker and only inserts newer rows into SQL Server. This prevents duplicate historical records when the script is executed again.

## SQL Analysis

SQL Server is used to perform additional analysis on the stored financial data.

Current SQL analyses include:

### Average Daily Return

Average daily return is calculated for each stock.

### Best Trading Day

`ROW_NUMBER()` and `PARTITION BY` are used to identify the trading day with the highest daily return for each stock.

### Worst Trading Day

The same ranking approach is used to identify the trading day with the lowest daily return for each stock.

### Positive and Negative Trading Days

The number of positive and negative trading days is calculated using `CASE` expressions.

### Annualized Volatility

Daily standard deviation is annualized using:

```text
Annualized Volatility = Daily Volatility × √252
```

### Sharpe Ratio

A simplified Sharpe Ratio is calculated using an assumed risk-free rate of 0%:

```text
Sharpe Ratio = Annualized Return / Annualized Volatility
```

### Risk & Return Summary

The main SQL summary combines:

* Annualized Return
* Annualized Volatility
* Sharpe Ratio
* Best Daily Return
* Worst Daily Return
* Total Trading Days
* Positive Trading Days
* Negative Trading Days

## Python ↔ SQL Server Integration

The project uses `pyodbc` to connect Python to SQL Server.

The current pipeline supports both directions:

```text
Python → SQL Server
```

for storing market data, and:

```text
SQL Server → Python
```

for retrieving SQL analysis results.

SQL analysis results are retrieved into Pandas DataFrames using:

```python
pd.read_sql()
```

The SQL risk and return summary is encapsulated in a Python function:

```python
def get_risk_return_summary():
    ...
```

This keeps the main program more organized and makes the SQL analysis reusable.

## Current Results

Based on the current analysis:

| Stock | Annualized Return | 8Y CAGR | 8Y Volatility | 8Y Sharpe |
| ----- | ----------------: | ------: | ------------: | --------: |
| NVDA  |            56.34% |  53.62% |        51.46% |      1.09 |
| AAPL  |            27.37% |  25.18% |        31.07% |      0.88 |
| META  |            24.21% |  16.58% |        41.82% |      0.58 |

Among the three stocks analyzed, **NVDA currently has the highest Annualized Return, CAGR, and Sharpe Ratio**, while also having the highest 8-year volatility.

This indicates that NVDA achieved the strongest historical return in the analyzed period, but these returns were accompanied by greater price volatility.

## Project Structure

The project is currently being developed and the structure may evolve as new analysis stages are added.

```text
Financial-Data-Analysis/
│
├── Python/
│   └── main.py
│
├── SQL/
│   ├── 01_create_database.sql
│   ├── 02_create_tables.sql
│   └── 03_analysis.sql
│
├── README.md
├── requirements.txt
└── .gitignore
```

## Future Improvements

Planned improvements include:

* Financial data visualization
* Stock price performance charts
* Risk and return comparison charts
* Volatility visualization
* Sharpe Ratio comparison
* Correlation heatmap
* Maximum Drawdown analysis
* Rolling volatility
* Rolling returns
* More advanced SQL analysis
* Final financial analysis report

## Disclaimer

This project is created for educational and portfolio purposes.

The analysis is based on historical market data and does not constitute financial advice or a recommendation to buy or sell any security.
