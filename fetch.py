import yfinance as yf
import pandas as pd

stock = yf.Ticker("AAPL")

data = stock.history(period="2y");

pd.set_option("display.width", 200)
pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)

data["Close"].to_csv("prices.txt", index=False, header=False)


print(data);


