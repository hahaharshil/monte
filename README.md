# Monte Carlo stock risk model

**Question:** if I invest in this stock for a year, how likely am I to lose money, and how much could I lose?

We answer it with **Value at Risk (VaR)**: simulate thousands of possible years from the stock's
historical behaviour, then read off the worst 5%.

## Run it

```sh
python3 -m venv .venv && .venv/bin/pip install yfinance numpy matplotlib   # once
.venv/bin/python fetch.py              # download AAPL prices
make                                   # build, simulate, plot
```

## Files

| file | step | what it does |
|---|---|---|
| `fetch.py` | 1 | downloads 2 years of AAPL closing prices from yfinance into `prices.txt` |
| `calc.cpp` | 2 | log returns → mean `mu` and volatility `sigma` → Monte Carlo → VaR and chance of loss (settings are at the top of the file) |
| `plot.py`  | 3 | draws the returns, 100 simulated years, and the final values with the VaR line |
| `Makefile` |   | builds and runs everything |

Generated files: `returns.txt`, `finals.txt`, `paths.txt`, `results.txt`.

## Method

1. Daily log return `r = ln(p_t / p_{t-1})`. Log returns add up over time.
2. `mu` = mean of r, `sigma` = sample standard deviation of r.
3. Each simulated year sums 252 draws from `Normal(mu, sigma)`, so the final value is `investment * e^sum`.
4. Sort the 10,000 final values. The **95% VaR** is `investment - 5th percentile`.

## Known limitations

- Real returns have **fat tails** (see the left plot: the -9% and +14% days), so a normal model underestimates crashes.
- `mu` and `sigma` come from the past 2 years and aren't guaranteed to hold in the future.
- Single stock only. Next steps: a correlated portfolio (Cholesky), beta vs SPY, and a backtest.
