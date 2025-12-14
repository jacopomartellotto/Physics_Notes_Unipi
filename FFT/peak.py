import numpy as np 
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

Directory='dati/' 
FileName=(Directory+'esperienza12/dati/ese12-non_mediati-0.22uF.txt') 
#T, dt,V,dv = np.loadtxt(FileName,unpack='True')
T, V = np.loadtxt(FileName,unpack='True')
t = T*1e-6
#dt = dt*1e-6


ASD = np.fft.rfft(V)
numpunti = int(len(V)/2)+1
risfreq=1/(1e-6*max(T))
freqmax=numpunti*risfreq
#print(risfreq)
ASD *= risfreq*max(t)/len(T)*2
ASD = abs(ASD)
freq = np.linspace(0,freqmax,numpunti)

# Filter data from ASD in the range 300-400Hz
filtered_ASD = ASD[(freq >= 400) & (freq <= 1500)]
filtered_freq = freq[(freq >= 400) & (freq <= 1500)]

def f(freq, v, w0, gamma):
    return v/((w0**2-(2*np.pi*freq)**2)**2+(2*np.pi*gamma*freq)**2)**0.5

popt, pcov = curve_fit(f, filtered_freq, filtered_ASD, p0=[10, 2*np.pi*350, 2*np.pi*10])
#print(popt)
#print(np.sqrt(np.diag(pcov)))
print('T = ', 2*np.pi/popt[1], ' +- ', 2*np.pi/(popt[1]**2)*np.sqrt(pcov[1, 1]))
print('tau = ', 2/popt[2], ' +- ', 2/(popt[2]**2)*np.sqrt(pcov[2, 2]))
x = np.linspace(400, 1500, 10000)

#plt.plot(freq, ASD, label='ASD')
plt.plot(filtered_freq, filtered_ASD, label='Filtered ASD')
plt.plot(x, f(x, *popt), label='Fit')
plt.minorticks_on()
plt.grid(which='both')
#plt.yscale('log')
plt.show()