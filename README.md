# Financial Data Analysis

A financial data analysis project built with Python to analyze historical stock market data. The project uses **Yahoo Finance** data and focuses on data cleaning, return analysis, volatility, risk-adjusted performance, and eventually SQL-based analysis and visualization.

## Project Objective

The main objective of this project is to analyze and compare the historical performance and risk characteristics of selected technology companies.

Currently, the project analyzes:

* Apple (AAPL)
* NVIDIA (NVDA)
* Meta Platforms (META)

The project is being developed as an end-to-end data analysis project using Python, Pandas, NumPy, PostgreSQL, SQL, and data visualization tools.

## Data Source

Historical stock market data is obtained using the `yfinance` Python library.

* Period: Approximately 8 years
* Interval: Daily
* Data source: Yahoo Finance

The following market variables are used:

* Open
* High
* Low
* Close
* Volume

## Current Analysis

### 1. Data Collection

Historical daily stock data is downloaded using `yfinance`.

```python
raw = yf.download(
    TICKERS,
    period="96mo",
    interval="1d",
    group_by="ticker"
)
```

### 2. Data Quality Checks

The dataset is checked for:

* Missing values
* Duplicated dates
* Invalid High/Low relationships
* Invalid High/Open relationships
* Negative trading volume
* Valid date ranges for each stock

### 3. Daily Return

Daily percentage returns are calculated using:

```python
daily_return = Closes.pct_change() * 100
```

Daily return measures the percentage change in a stock's closing price from one trading day to the next.

### 4. Monthly and Yearly Returns

Monthly and yearly returns are calculated to examine how stock performance changes over longer periods.

The project calculates:

* Monthly returns
* Yearly returns

### 5. Volatility Analysis

Annualized volatility is calculated using the standard deviation of daily returns.

Two periods are currently analyzed:

* 1-year volatility
* 8-year volatility

The annualization uses approximately 252 trading days:

```python
volatility = daily_return.std() * np.sqrt(252)
```

Higher volatility indicates larger fluctuations in daily returns and therefore higher historical price variability.

### 6. Annualized Return

The average daily return is annualized using:

```python
annualized_return = daily_return.mean() * 252
```

This provides an annualized estimate based on the arithmetic mean of daily returns.

### 7. CAGR

Compound Annual Growth Rate (CAGR) is used to measure the annualized compound growth between the beginning and ending prices over the available historical period.

Unlike the arithmetic annualized return, CAGR considers the actual beginning and ending values of the investment.

### 8. Sharpe Ratio

A simplified Sharpe Ratio is calculated to evaluate return relative to volatility:

```python
sharpe_ratio = annualized_return / volatility
```

The current implementation assumes a **0% risk-free rate**.

Both 1-year and 8-year Sharpe Ratios will be included in the completed risk-return analysis.

## Current Risk & Return Metrics

The current analysis contains:

| Metric            | Period  |
| ----------------- | ------- |
| Annualized Return | 1Y / 8Y |
| CAGR              | 8Y      |
| Volatility        | 1Y / 8Y |
| Sharpe Ratio      | 1Y / 8Y |

These metrics will be used to compare the historical risk and performance characteristics of AAPL, NVDA, and META.

## Technologies

* Python
* Pandas
* NumPy
* yfinance
* PostgreSQL
* SQL
* Matplotlib
* Seaborn

## Project Roadmap

The project will be developed in the following stages:

* [x] Data collection with `yfinance`
* [x] Data quality checks
* [x] Daily return analysis
* [x] Monthly return analysis
* [x] Yearly return analysis
* [x] 1Y and 8Y volatility analysis
* [x] Annualized return analysis
* [x] CAGR analysis
* [x] Risk & Return analysis
* [ ] Correlation analysis
* [ ] PostgreSQL database integration
* [ ] SQL-based financial analysis
* [ ] Data visualization with Matplotlib and Seaborn
* [ ] Final analysis and report

## Project Structure

```text
Financial-Data-Analysis/
│
├── financial_data_analysis.py
├── README.md
└── requirements.txt
```

## Future Improvements

Future versions of the project will include:

* Correlation analysis between stocks
* PostgreSQL database integration
* SQL queries for financial analysis
* Risk-free rate integration
* More advanced risk metrics
* Drawdown analysis
* Portfolio analysis
* Financial data visualization
* Final analytical report

## Disclaimer

This project is for educational and analytical purposes only. The results are based on historical market data and should not be interpreted as financial advice.
