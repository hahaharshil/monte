# Monte Carlo Risk Model

If you invest in a stock for one year, how likely are you to lose money, and how much could you lose?

This project answers that for any stock on Yahoo Finance. It downloads two years of daily prices, simulates 10,000 possible years with the Monte Carlo method, and reports the **95% Value at Risk (VaR)** and the **chance of a loss**. It then checks the model's assumptions with hypothesis tests and compares the stock with the market using correlation and regression.

## Run

```sh
python3 -m venv .venv
.venv/bin/pip install yfinance numpy matplotlib scipy
make
```

`make` asks for a ticker (for example `AAPL`), then downloads the data, runs the simulation, draws the plots and runs the tests.

## Files

| File | What it does |
|---|---|
| `fetch.py` | Downloads two years of closing prices for the ticker and for SPY (the market) |
| `calc.cpp` | Log returns, mean and volatility, 10,000 simulated years, VaR and chance of a loss |
| `plot.py` | Plots the daily returns, 100 simulated years and the final values with the VaR line |
| `stats.py` | t-test, F-test, two sample t-test, chi-square test, least squares trend, correlation and regression |
| `Makefile` | Runs everything in order |
| `report/` | Project report in LaTeX (`report.tex`) and the compiled `report.pdf` |

## Method

1. Daily log return: `r = ln(P_today / P_yesterday)`.
2. Mean `mu` and standard deviation `sigma` of the returns.
3. Each simulated year is 252 days. Every day the money is multiplied by `e^r`, where `r` is drawn from a normal distribution with `mu` and `sigma`.
4. The 10,000 end values are sorted. The 95% VaR is the starting money minus the 5th percentile.

## Tests

All at the 5% significance level.

| Test | Question |
|---|---|
| t-test | Is the average daily return different from zero? |
| F-test | Was the volatility the same in the first and second year? |
| Two sample t-test | Was the average return the same in both years? (pooled or Welch, chosen by the F-test) |
| Chi-square | Are the daily returns normally distributed? |
| Least squares | Exponential trend curve fitted to the price |
| Correlation | Does the stock move with the market? |
| Regression | Beta of the stock against the market, and R² |

## Results for AAPL ($10,000, one year)

| | |
|---|---|
| 95% VaR | $2,353 |
| Chance of a loss | 23.1% |
| Mean return significant? | No (t = 1.01) |
| Same volatility both years? | No (F = 1.68) |
| Returns normal? | No (χ² = 65.9) |
| Beta vs SPY | 1.02 (R² = 0.36) |

The tests show that the simple normal model leaves out part of the risk, so the VaR above should be read as a lower estimate.

## Report

`report/report.tex` builds with pdfLaTeX. It also works on Overleaf: upload the `report` folder, plus the college logo as `report/image.png`.
