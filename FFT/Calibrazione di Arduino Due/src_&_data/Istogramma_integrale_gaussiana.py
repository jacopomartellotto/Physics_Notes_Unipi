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

# Seleziona solo i dati tra 3500 e 3580
filtered_df = df[(df['ddp'] >= 3500) & (df['ddp'] <= 3580)]
num_bins = np.max(filtered_df['ddp']) - np.min(filtered_df['ddp'])
hist, bin_edges = np.histogram(filtered_df['ddp'], bins=num_bins, density=True)
bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2


def gaussian(x, amplitude, mean, std_dev):
    return amplitude * np.exp(-(x - mean)**2 / (2 * std_dev**2))

def gaussian2(x, mean, std_dev):
    return 1/np.sqrt(2*np.pi)/std_dev * np.exp(-(x - mean)**2 / (2 * std_dev**2))

def gaussian_i(x, mean, std_dev):
    ei = []
    for xi in x:
        ei.append(integrate.quad(lambda b: gaussian2(b, mean, std_dev), xi-0.5, xi+0.5)[0])
    return np.array(ei)


params, covariance = curve_fit(gaussian_i, bin_centers, hist, p0=[3527, 15])
mean, std_dev = params
print(params)
x = np.linspace(3500, 3580, 1000)
gaussian_curve = gaussian2(x, *params)


ei = gaussian_i(bin_centers, mean, std_dev)
chisq = np.sum((hist - ei)**2/ei)
print(chisq)

plt.figure(figsize=(8, 6))
plt.hist(filtered_df['ddp'], density=True, bins=num_bins, alpha=0.5, edgecolor='k', facecolor='green')
plt.plot(x, gaussian_curve)
plt.xlabel('Valore')
plt.ylabel('Frequenza')
plt.show()
