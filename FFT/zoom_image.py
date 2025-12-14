import numpy as np 
import matplotlib.pyplot as plt

Directory='dati/' 
FileName=(Directory+'esperienza5_2/F73-QS.txt') 
#T, dt,V,dv = np.loadtxt(FileName,unpack='True')
T, V = np.loadtxt(FileName,unpack='True')
t= T*1e-6


ASD = abs(np.fft.rfft(V))
numpunti = int(len(V)/2)+1
risfreq=1/(1e-6*max(T))
freqmax=numpunti*risfreq
freq = np.linspace(0,freqmax,numpunti)

plt.ylabel('ASD [arb.un.]')
plt.xlabel('f [Hz]')
plt.plot(freq,ASD)
plt.yscale('log')
plt.minorticks_on()
plt.show()