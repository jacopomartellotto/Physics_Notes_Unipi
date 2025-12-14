import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

# Parameters for the square wave
frequency = 1 # Frequency in Hz
duty_cycle = 0.5  # Duty cycle (0.5 for a perfect square wave)

t = np.linspace(0, 1, 1000)

# Generate the square wave
square_wave = signal.square(2 * np.pi * frequency * t, duty=duty_cycle)

# Parameters for the Voigt noise
mean_gaussian = 0.0
std_gaussian = 0.1 
scale_lorentzian = 0.05 
gaussian_noise = np.random.normal(mean_gaussian, std_gaussian, len(t))
lorentzian_noise = np.random.uniform(-scale_lorentzian, scale_lorentzian, len(t))
# Combine Gaussian and Lorentzian noise to create Voigt noise
voigt_noise = (gaussian_noise + 1j * lorentzian_noise)
noisy_square_wave = square_wave + voigt_noise.real


plt.figure(figsize=(8, 4))
plt.plot(t, noisy_square_wave, label="Noisy Square Wave")
plt.xlabel("t [s]")
plt.ylabel("Amplitude [a.u.]")
plt.show()
