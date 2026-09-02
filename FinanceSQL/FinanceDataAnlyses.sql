SELECT
    Ticker,
    AVG(daily_return) AS AverageDailyReturn
FROM [FinancialData].[dbo].[StockPrices]
GROUP BY Ticker
ORDER BY AverageDailyReturn DESC;
-- NVDA has the most average daily return.

-- Best and worst trading day for each stock

WITH RankedReturns AS
(
    SELECT
        Ticker,
        TradeDate,
        daily_return,
        ROW_NUMBER() OVER (
            PARTITION BY Ticker
            ORDER BY daily_return DESC
        ) AS RowNum
    FROM [FinancialData].[dbo].[StockPrices]
)

SELECT
    Ticker,
    TradeDate,
    daily_return
FROM RankedReturns
WHERE RowNum = 1;

WITH RankedReturns AS
(
    SELECT
        Ticker,
        TradeDate,
        daily_return,
        ROW_NUMBER() OVER (
            PARTITION BY Ticker
            ORDER BY daily_return ASC
        ) AS RowNum
    FROM [FinancialData].[dbo].[StockPrices]
    WHERE daily_return IS NOT NULL
)

SELECT
    Ticker,
    TradeDate,
    daily_return
FROM RankedReturns
WHERE RowNum = 1;