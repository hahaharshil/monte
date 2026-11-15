import matplotlib.pyplot as plt
import numpy as np 


r = np.loadtxt("returns.txt");
plt.hist(r, bins=50);
plt.show();
