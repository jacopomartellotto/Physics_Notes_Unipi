import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

t = np.linspace(0, 10, 2**10)

def square_wave(x, T):
    return 2 * np.floor((2 * x / T) % 2) - 1

V = 1 + square_wave(t, 2) + 0.01 * np.random.randn(t.size)

ASD = np.fft.rfft(V)
numpunti = int(len(V)/2)+1
risfreq=1/(max(t))
freqmax=numpunti*risfreq
freq = np.linspace(0,freqmax,numpunti)

def funzione(x):
    return 3.6e2/x**1.06
y = funzione(freq)

def funzione(x):
    return 3.6e2/x**1
z = funzione(freq)

fig = plt.figure()
fig.add_axes((0.12,0.6,0.8,0.35))
plt.plot(t, V)
plt.minorticks_on()

fig.add_axes((0.12,0.12,0.8,0.35))
plt.ylabel('ASD [arb.un.]')
plt.xlabel('f [Hz]')
ASD = abs(ASD)
plt.plot(freq,ASD)
plt.plot(freq,y)
plt.plot(freq,z)
plt.legend(['ASD', 'f^-1.06', 'f^-1'])
plt.yscale('log')
plt.minorticks_on()
plt.show()