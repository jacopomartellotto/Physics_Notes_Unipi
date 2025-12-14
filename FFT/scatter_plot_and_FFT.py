import numpy as np 
import matplotlib.pyplot as plt

Directory='dati/' 
FileName=(Directory+'esperienza9/dataEDJ-vd-1.75V.txt') 
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
freq = np.linspace(0,freqmax,numpunti)

#fig = plt.figure()
#fig.add_axes((0.12,0.6,0.8,0.35))
plt.ylabel('V [digit]')
plt.xlabel('t [s]')
plt.minorticks_on()
plt.plot(t,V)
#plt.errorbar(t, V, fmt='.', markersize=1)
#plt.errorbar(t, V, xerr=dt, yerr=dv, fmt='.', markersize=2)

V0 = np.mean(V)
vdf = V0 + np.real(ASD[138]*np.exp(1j*2*np.pi*freq[138]*t))
print(ASD[138])
print(freq[138])
plt.plot(t, vdf)

'''def funzione(x):
    return 2.8e8/x**1.06 / np.sqrt(1+(x/482)**2)
y = funzione(freq)'''
'''
fig.add_axes((0.12,0.12,0.8,0.35))
plt.ylabel('ASD [arb.un.]')
plt.xlabel('f [Hz]')
ASD = abs(ASD)
plt.plot(freq,ASD)
#plt.plot(freq,y)
#plt.xscale('log')
plt.yscale('log')
'''
plt.minorticks_on()
#plt.savefig('svg/ese12/ind_antis.svg')
plt.show()