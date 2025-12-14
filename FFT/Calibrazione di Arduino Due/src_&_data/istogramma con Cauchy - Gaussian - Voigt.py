import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.optimize import curve_fit
from scipy.stats import cauchy, norm
import scipy.integrate as integrate
from lmfit.models import VoigtModel

n = '243'
colonne = ['t', 'ddp']
df = pd.read_table("quo\\quo" + n + ".txt", skiprows=0, sep='\s+', header=None, names=colonne)
ddp = df['ddp']

# Seleziona solo i dati tra 3500 e 3580
#filtered_df = df[(df['ddp'] >= 3500) & (df['ddp'] <= 3580)]

filtered_df = df
num_bins = np.max(filtered_df['ddp']) - np.min(filtered_df['ddp'])
hist, bin_edges = np.histogram(filtered_df['ddp'], bins=num_bins, density=True)
bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2

def gaussian(x, amplitude, mean, std_dev):
    return amplitude * np.exp(-(x - mean)**2 / (2 * std_dev**2))

def cau(x, p, q):
    return cauchy.pdf(x, p, q)

def gau(x, p, q):
    return norm.pdf(x, p, q)

#params, covariance = curve_fit(gaussian, bin_centers, hist, p0=[3527, 3527, 100])
#amplitude, mean, std_dev = params

'''params, covariance = curve_fit(gaussian_i, bin_centers, hist, p0=[3527, 15])
mean, std_dev = params
print(params)'''

'''params, covariance = curve_fit(cau, bin_centers, hist, p0=[3540, 20])
print(params)
print(np.sqrt(np.diag(covariance)))
curve = cau(x, *params)'''


'''ei = gaussian_i(bin_centers, mean, std_dev)
print(ei)
chisq = np.sum((hist - ei)**2/ei)
print(chisq)'''

model = VoigtModel()
params = model.make_params(amplitude=1, center=1500, sigma=1, gamma=20)
params['amplitude'].vary = False
params['amplitude'].value = 1
params['center'].vary = True
params['sigma'].vary = True
params['gamma'].vary = True
result = model.fit(hist, params, x=bin_centers)
print(result.fit_report())
x = np.linspace(3500, 3580, 1000)
curve_voi = result.eval(x=x)

plt.figure(figsize=(8, 6))
plt.hist(filtered_df['ddp'], density=True, bins=num_bins, alpha=0.5, edgecolor='k', facecolor='green')
#plt.plot(x, curve, 'b-')
plt.plot(x, curve_voi)
plt.xlabel('$V_{dig}$ [digit]')
plt.ylabel('Probabilità')
#plt.savefig('Funzione di Voigt.png', dpi = 600)
plt.show()
