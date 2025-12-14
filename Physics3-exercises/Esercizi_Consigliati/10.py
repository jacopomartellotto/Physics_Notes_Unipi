import numpy as np
import matplotlib.pyplot as plt

# Costanti fisiche
epsilon0 = 8.854187817e-12
c = 299792458.0
mu0 = 1.0/(epsilon0 * c**2)

# Parametri
Q = 1e-9      # Coulomb
b = 0.1       # metri
beta = 0.6
V = beta * c
gamma = 1.0 / np.sqrt(1.0 - beta**2)

# Tempo centrato sull'istante di massimo avvicinamento t=0
t0 = 5.0 * b / (gamma * V)
t = np.linspace(-t0, t0, 1000)

# Denominatore ausiliario
den = (b**2 + (gamma**2) * (V**2) * (t**2))**(1.5)

# Componenti del campo elettrico all'origine
pref = Q / (4.0 * np.pi * epsilon0)
Ex = -pref * (V * t) / den
Ey = -pref * (b / (gamma**2)) / den
Ez = np.zeros_like(t)

# Componenti del campo magnetico B = (1/c^2) v × E, con v lungo +x
Bx = np.zeros_like(t)
By = np.zeros_like(t)
Bz = (V / c**2) * Ey

# Plot in unica figura
fig, axes = plt.subplots(3, 2, figsize=(10, 8))
axes = axes.flatten()

components = [
    (Ex, r"$E_x$ (V/m)", "Electric field $E_x(t)$"),
    (Ey, r"$E_y$ (V/m)", "Electric field $E_y(t)$"),
    (Ez, r"$E_z$ (V/m)", "Electric field $E_z(t)$"),
    (Bx, r"$B_x$ (T)", "Magnetic field $B_x(t)$"),
    (By, r"$B_y$ (T)", "Magnetic field $B_y(t)$"),
    (Bz, r"$B_z$ (T)", "Magnetic field $B_z(t)$")
]

for ax, (y, ylabel, title) in zip(axes, components):
    ax.plot(t, y)
    ax.set_xlabel(r"$t$ (s)")
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.grid(True)

plt.tight_layout()
plt.savefig("E_B_components.png", dpi=300)
plt.show()
