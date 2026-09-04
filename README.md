Stock Data Pipeline & Risk/Return Analysis

Pulls historical price data for AAPL, NVDA, META via yfinance, stores it in SQL Server, and produces risk/return charts.

Files
FinanceMain.py — pipeline: downloads data, computes returns/CAGR/Sharpe, loads into the StockPrices table
visualize_stock_data.py — reads from SQL Server, produces 3 charts
Requirements
bash
pip install pandas numpy yfinance pyodbc matplotlib

SQL Server (ODBC Driver 18) with a StockPrices table:

sql
CREATE TABLE StockPrices (
    TradeDate DATE NOT NULL,
    Ticker VARCHAR(10) NOT NULL,
    OpenPrice FLOAT, HighPrice FLOAT, LowPrice FLOAT, ClosePrice FLOAT,
    Volume BIGINT, daily_return FLOAT,
    CONSTRAINT UQ_Ticker_TradeDate UNIQUE (Ticker, TradeDate)
);
Usage
bash
python FinanceMain.py            # run first — loads/updates data
python visualize_stock_data.py   # reads from SQL, generates charts
Charts

Results (8-year window)
Ticker	Ann. Return	Ann. Volatility	Sharpe
NVDA	                  ~57%	  ~51%	~1.1
AAPL	                  ~27%	  ~31%	~0.9
META	                  ~25%	  ~42%	~0.6

NVDA leads on raw return; AAPL has the best Sharpe after NVDA thanks to lower volatility, while META trails on both return and risk-adjusted performance.

Notes
Sharpe ratio = annualized return / annualized volatility (no risk-free rate subtracted)
Assumes 252 trading days/year, i.i.d. daily returns
Run the pipeline at least once before visualizing

## Disclaimer

This project is created for educational and portfolio purposes.

The analysis is based on historical market data and does not constitute financial advice or a recommendation to buy or sell any security.
