import yfinance as yf


tic = input("Enter Ticker: ")

stock = yf.Ticker(tic)
data = stock.history(period="2y")

data["Close"].to_csv("prices.txt", index=False, header=False)

print(data)

open("ticker.txt", "w").write(tic)
