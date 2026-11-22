import matplotlib.pyplot as plt
import numpy as np

returns = np.loadtxt("returns.txt")
paths = np.loadtxt("paths.txt")
finals = np.loadtxt("finals.txt")
money, var, chance = np.loadtxt("results.txt")
ticker = open("ticker.txt").read()

orange = "#ffa028"
red = "#ff4d4d"
blue = "#4f9ff0"

plt.style.use("dark_background")
plt.rcParams["font.family"] = "monospace"
plt.rcParams["axes.facecolor"] = "black"
plt.rcParams["figure.facecolor"] = "black"
plt.rcParams["axes.titlecolor"] = orange

fig, ax = plt.subplots(1, 3, figsize=(16, 5))
fig.suptitle(f"{ticker}   VaR 95%: ${var:,.0f}   chance of loss: {chance:.1f}%",
             color=orange, fontsize=14)

# daily returns
ax[0].hist(returns * 100, bins=60, color=blue)
ax[0].set_title("daily returns")
ax[0].set_xlabel("%")

# 100 pretend years
for path in paths:
    ax[1].plot(path, color=blue, alpha=0.2, linewidth=0.7)
ax[1].axhline(money, color="gray", linestyle=":")
ax[1].set_title("100 simulated years")
ax[1].set_xlabel("day")

# money after one year
ax[2].hist(finals, bins=80, color=blue)
ax[2].axvline(money - var, color=red, label="VaR 95%")
ax[2].axvline(money, color="gray", linestyle=":", label="start")
ax[2].set_title("money after one year")
ax[2].set_xlabel("$")
ax[2].legend()

plt.tight_layout()
plt.savefig("risk.png")
plt.show()
