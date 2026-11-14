import matplotlib.pyplot as plt
import numpy as np 


x,y = np.loadtxt("output.txt", unpack=True);
plt.scatter(x,y);


plt.show();
