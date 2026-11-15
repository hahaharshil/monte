files that matters:
fetech.py --> fetches data for a ticker for a period of each day and puts it into prices.txt from yfinance.

calc.cpp --> fetches data from prices.txt, calculates everything. r: daily returns mu: avg of daily returns sigma: variance in returns. 

plot.py --> plots everything using matplotlib. right now its just plots a histro for returns as a test.

mostly c files are useless, I switched to cpp, c was taking way too much time. and there are bunch of executable fiiles that i have to put into gitignore. 
