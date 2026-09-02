CREATE UNIQUE INDEX UQ_StockPrices_Ticker_TradeDate
ON StockPrices (Ticker, TradeDate)
WITH (IGNORE_DUP_KEY = ON);

USE FinancialData;
CREATE TABLE StockPrices (
    ID INT IDENTITY(1,1) PRIMARY KEY,
    TradeDate DATE NOT NULL,
    Ticker VARCHAR(10) NOT NULL,
    OpenPrice DECIMAL(18,4),
    HighPrice DECIMAL(18,4),
    LowPrice DECIMAL(18,4),
    ClosePrice DECIMAL(18,4),
    Daily_Return float,
    Volume BIGINT
);
