import yfinance as yf


tic = input("Enter Ticker: ")

stock = yf.Ticker(tic).history(period="2y")["Close"]
market = yf.Ticker("SPY").history(period="2y")["Close"]

# use only the date, so both tables line up even in different time zones
stock.index = stock.index.date
market.index = market.index.date

# keep only the days where both have a price
data = stock.to_frame("stock").join(market.to_frame("market"), how="inner")

data["stock"].to_csv("prices.txt", index=False, header=False)
data["market"].to_csv("market.txt", index=False, header=False)

print(data)

open("ticker.txt", "w").write(tic)
