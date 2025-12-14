import numpy as np 
import matplotlib.pyplot as plt
import pandas as pd
from scipy.optimize import curve_fit

'''
n = '1981'
colonne = ['t', 'ddp']
df = pd.read_table("quo\\quo" + n + ".txt", skiprows=0, sep='\s+', header=None, names=colonne)
t = df['t']
ddp = df['ddp']

av_ddp = np.mean(ddp)
print(av_ddp)

f = open("medie.txt", "a")
f.write(n + " " + str(av_ddp) + "\n")
f.close()
'''

colonne = ['Vv', 'sVv', 'Vd', 'sVd']
df = pd.read_table("medie.txt", skiprows=0, sep='\s+', header=None, names=colonne)
Vv = df['Vv']
sigma_Vv = df['sVv']
Vd = df['Vd']
sigma_Vd = df['sVd']

def line(x, a, b):
    return a+b*x

def par(x, a, b, c):
    return a+b*x+c*x*x

fig = plt.figure('Calibrazione')
fig.add_axes((0.12, 0.3, 0.8, 0.6))
plt.minorticks_on()
plt.errorbar(Vd, Vv, yerr=sigma_Vv, fmt='.')

popt, pcov = curve_fit(par, Vd, Vv, sigma=sigma_Vv, p0=[0, -0.5, 0.0007], absolute_sigma=False)
for i in range(10):
    sigma_eff = np.sqrt(sigma_Vv**2.0 + ((popt[1] + 2*popt[2] * Vd) * sigma_Vd)**2.0)
    popt, pcov = curve_fit(par, Vd, Vv, sigma=sigma_eff)
    chisq = (((Vv - par(Vd, *popt)) / sigma_eff)**2.0).sum()
print(chisq)

a, b, c = popt
sigma_a, sigma_b, sc = np.sqrt(np.diag(pcov))
corr = pcov[0,1]/sigma_a/sigma_b
print('a: ', a, 'sigma_a: ', sigma_a, '\nb: ', b, 'sigma_b: ', sigma_b, '\nc: ', c, 'sigma_c: ', sc)

'''
a= popt
sigma_a = np.sqrt(np.diag(pcov))
print('a: ', a, 'sigma_a: ', sigma_a)
'''

x = np.linspace(0.0, 4100.0, 10000)
plt.plot(x, par(x, *popt))
plt.ylabel('$V_V$ [V]')
#plt.grid(which='both', ls='dashed', color='gray')

'''
ren_res = (Vv - line(Vd, *popt)) / sigma_Vv
#chisq = (ren_res**2.0).sum()

fig.add_axes((0.12, 0.1, 0.8, 0.2))
plt.minorticks_on()
plt.errorbar(Vd, ren_res, yerr=1, fmt='o', capsize=2, markersize=2.5)
y = np.linspace(0.0, 0.0, 10000)
plt.plot(x, y)
plt.ylabel('Residui\nnormalizzati')
'''
plt.xlabel('$V_{dig}$ [digit]')
plt.show()