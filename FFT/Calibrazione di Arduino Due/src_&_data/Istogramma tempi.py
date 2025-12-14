import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.stats import norm
from scipy.optimize import curve_fit
import scipy.integrate as integrate

n = '279'
colonne = ['t', 'ddp']
df = pd.read_table("quo\\quo" + n + ".txt", skiprows=0, sep='\s+', header=None, names=colonne)
ddp = df['ddp']
t = np.diff(df['t'])
t = t[1:]

# Seleziona solo i dati tra 3500 e 3580
filtered_df = df[(df['ddp'] >= 3500) & (df['ddp'] <= 3580)]

num_bins = np.max(t) - np.min(t)
hist, bin_edges = np.histogram(t, bins=num_bins, density=True)
bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2

print(np.mean(t), np.std(t/len(t-1)**0.5))

plt.figure(figsize=(8, 6))
plt.hist(t, density=True, bins=num_bins, alpha=0.5, edgecolor='k', facecolor='green')
#plt.plot(x, gaussian_curve)
plt.xlim([100, 115])
plt.xlabel('$\Delta t$ [$\mu$s]')
plt.ylabel('Probabilità')
plt.show()
#plt.savefig('Tempi.png', dpi=600)
