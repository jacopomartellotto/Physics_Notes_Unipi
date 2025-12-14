import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

colonne = ['t', 'ddp']
df = pd.read_table("quinada.txt", skiprows=0, sep='\s+', header=None, names=colonne)

# Filtra i dati in base alla condizione 0 <= ddp <= 2200
df_filtrato = df[(df['ddp'] >= 0) & (df['ddp'] <= 2200)]

# Estrai le colonne filtrate
t = df_filtrato['t']
ddp = df_filtrato['ddp']
print(ddp)

plt.plot(t, ddp, color='blue')
plt.minorticks_on()
plt.xlabel('Time [$\mu$s]')
plt.ylabel('$V_{dig}$ [digit]')
plt.savefig("rumore_quinada.png", dpi = 600)
plt.show()
