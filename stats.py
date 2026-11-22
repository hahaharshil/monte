import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

prices = np.loadtxt("prices.txt")
market = np.loadtxt("market.txt")
ticker = open("ticker.txt").read()

# daily log returns of the stock (r) and of the market (m)
r = np.log(prices[1:] / prices[:-1])
m = np.log(market[1:] / market[:-1])
n = len(r)


def mean(x):
    return np.sum(x) / len(x)


def var(x):
    return np.sum((x - mean(x)) ** 2) / (len(x) - 1)


def decide(value, table):
    if abs(value) > table:
        return "reject H0"
    return "accept H0"


print(f"{ticker}: {n} daily returns\n")

# ---------- 1. t-test: is the average return different from 0? ----------
t1 = mean(r) / np.sqrt(var(r) / n)
t1_table = stats.t.ppf(0.975, n - 1)
print("1. t-test   H0: mean return = 0")
print(f"   t = {t1:.3f}   table = {t1_table:.3f}   {decide(t1, t1_table)}\n")

# split the two years into two halves
half = n // 2
a = r[:half]
b = r[half:]

# ---------- 2. F-test: is the risk the same in both years? ----------
if var(a) > var(b):
    F = var(a) / var(b)
else:
    F = var(b) / var(a)
F_table = stats.f.ppf(0.975, half - 1, n - half - 1)
same_var = F < F_table
print("2. F-test   H0: variance in year 1 = variance in year 2")
print(f"   F = {F:.3f}   table = {F_table:.3f}   {decide(F, F_table)}\n")

# ---------- 3. two sample t-test: is the average return the same in both years? ----------
na = len(a)
nb = len(b)
if same_var:
    sp = ((na - 1) * var(a) + (nb - 1) * var(b)) / (na + nb - 2)
    t2 = (mean(a) - mean(b)) / np.sqrt(sp * (1 / na + 1 / nb))
    df2 = na + nb - 2
else:
    va = var(a) / na
    vb = var(b) / nb
    t2 = (mean(a) - mean(b)) / np.sqrt(va + vb)
    df2 = (va + vb) ** 2 / (va ** 2 / (na - 1) + vb ** 2 / (nb - 1))
t2_table = stats.t.ppf(0.975, df2)
print("3. t-test   H0: mean in year 1 = mean in year 2")
print(f"   t = {t2:.3f}   df = {df2:.0f}   table = {t2_table:.3f}   {decide(t2, t2_table)}\n")

# ---------- 4. chi-square test: are the returns normal? ----------
k = 10
edges = stats.norm.ppf(np.linspace(0, 1, k + 1), mean(r), np.sqrt(var(r)))
observed = np.histogram(r, edges)[0]
expected = np.full(k, n / k)
chi2 = np.sum((observed - expected) ** 2 / expected)
chi2_table = stats.chi2.ppf(0.95, k - 3)
print("4. chi-square test   H0: returns are normal")
print(f"   chi2 = {chi2:.2f}   df = {k - 3}   table = {chi2_table:.2f}   {decide(chi2, chi2_table)}\n")

# ---------- 5. least squares curve: ln(price) = a + b * day ----------
day = np.arange(len(prices))
y = np.log(prices)
slope = np.sum((day - mean(day)) * (y - mean(y))) / np.sum((day - mean(day)) ** 2)
intercept = mean(y) - slope * mean(day)
trend = np.exp(intercept + slope * day)
print("5. least squares trend   price = e^(a + b*day)")
print(f"   a = {intercept:.4f}   b = {slope:.6f}   growth per year = {(np.exp(252 * slope) - 1) * 100:.1f}%\n")

# ---------- 6. correlation between stock and market ----------
corr = np.sum((r - mean(r)) * (m - mean(m))) / np.sqrt(np.sum((r - mean(r)) ** 2) * np.sum((m - mean(m)) ** 2))
t3 = corr * np.sqrt(n - 2) / np.sqrt(1 - corr ** 2)
t3_table = stats.t.ppf(0.975, n - 2)
print("6. correlation   H0: no correlation with the market")
print(f"   r = {corr:.3f}   t = {t3:.2f}   table = {t3_table:.3f}   {decide(t3, t3_table)}\n")

# ---------- 7. regression: stock return = alpha + beta * market return ----------
beta = np.sum((m - mean(m)) * (r - mean(r))) / np.sum((m - mean(m)) ** 2)
alpha = mean(r) - beta * mean(m)
print("7. regression   stock = alpha + beta * market")
print(f"   alpha = {alpha:.5f}   beta = {beta:.3f}   R^2 = {corr ** 2:.3f}")
print(f"   {corr ** 2 * 100:.0f}% of the daily moves are explained by the market")

# ---------- plots ----------
orange = "#ffa028"
red = "#ff4d4d"
blue = "#4f9ff0"

plt.style.use("dark_background")
plt.rcParams["font.family"] = "monospace"
plt.rcParams["axes.titlecolor"] = orange

fig, ax = plt.subplots(1, 3, figsize=(16, 5))
fig.suptitle(f"{ticker}   beta: {beta:.2f}   r: {corr:.2f}   chi2: {chi2:.1f}",
             color=orange, fontsize=14)

# price and the least squares trend curve
ax[0].plot(prices, color=blue, linewidth=1, label="price")
ax[0].plot(trend, color=orange, label="least squares trend")
ax[0].set_title("price and trend")
ax[0].set_xlabel("day")
ax[0].legend()

# stock vs market with the regression line
ax[1].scatter(m * 100, r * 100, color=blue, s=6, alpha=0.6)
x = np.linspace(m.min(), m.max(), 2)
ax[1].plot(x * 100, (alpha + beta * x) * 100, color=orange, label=f"beta = {beta:.2f}")
ax[1].set_title("stock vs market")
ax[1].set_xlabel("SPY return %")
ax[1].set_ylabel(f"{ticker} return %")
ax[1].legend()

# chi-square: observed vs expected count in each bin
ax[2].bar(np.arange(k) - 0.2, observed, width=0.4, color=blue, label="observed")
ax[2].bar(np.arange(k) + 0.2, expected, width=0.4, color=red, label="expected if normal")
ax[2].set_title("chi-square test")
ax[2].set_xlabel("bin (10% of a normal curve each)")
ax[2].legend()

plt.tight_layout()
plt.savefig("stats.png")
plt.show()
