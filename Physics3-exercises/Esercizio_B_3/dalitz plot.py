import numpy as np
import matplotlib.pyplot as plt

# --- Masse (MeV) ---
# Convenzione: tutto in MeV (le ascisse le riporteremo in GeV^2 solo in fase di plot).
M  = 939.565    # neutrone (nel CM: sqrt(s)=M)
m1 = 938.272    # protone
m2 = 0.510999   # elettrone
m3 = 0.0        # antineutrino ~ 0
s  = M**2       # invariante totale nel CM del neutrone

# --- Griglie di s12 e s23 (MeV^2) ---
# Si costruisce una griglia rettangolare nel "box" cinematica consentito dagli estremi banali:
#   (m1+m2)^2 <= s12 <= (M-m3)^2
#   (m2+m3)^2 <= s23 <= (M-m1)^2
# Attenzione: questi sono solo BOUND GREZZI; la regione fisica vera è più piccola e sarà selezionata dalla mask.
S12s = np.linspace((m1+m2)**2, (M-m3)**2, 1200)
S23s = np.linspace((m2+m3)**2, (M-m1)**2, 1200)
s12g, s23g = np.meshgrid(S12s, S23s, indexing="xy")

# --- Quantità ausiliarie ---
s13g = s + m1**2 + m2**2 + m3**2 - s12g - s23g

# --- Energie nel CM del neutrone (cinematica a 3 corpi) ---
# Se qualche Ei risultasse negativo, quel punto (s12,s23) NON è fisico.
E1 = 0.5*M + (m1**2 - s23g)/(2*M)
E2 = 0.5*M + (m2**2 - s13g)/(2*M)
E3 = 0.5*M + (m3**2 - s12g)/(2*M)

# --- Vincoli di energia positiva ---
Epos = (E1 >= 0) & (E2 >= 0) & (E3 >= 0)

# --- Moduli dei momenti al quadrato ---
p1sq = E1**2 - m1**2
p2sq = E2**2 - m2**2
p3sq = E3**2 - m3**2

# --- Momenti reali (clip per robustezza numerica) ---
# Per evitare piccoli artefatti numerici (valori tipo -1e-14), si clip a 1e-12.
eps = 1e-12
pOK = (p1sq >= -eps) & (p2sq >= -eps) & (p3sq >= -eps)
p1sq = np.clip(p1sq, 0.0, None)
p2sq = np.clip(p2sq, 0.0, None)
p3sq = np.clip(p3sq, 0.0, None)

# --- Condizioni angolari (equivalenti a -1 <= cos <= +1) ---
with np.errstate(divide='ignore', invalid='ignore'):
    cos_th = (p3sq - p2sq - p1sq) / (2*np.sqrt(p1sq*p2sq))
    cos_ph = (p2sq - p3sq - p1sq) / (2*np.sqrt(p1sq*p3sq))
    cond_ang = (
        np.isfinite(cos_th) & np.isfinite(cos_ph) &
        (cos_th**2 <= 1.0) & (cos_ph**2 <= 1.0)
    )

# --- Maschera finale di ammissibilità (0/1) ---
# mask=1 (dentro) se: energie positive, momenti reali e vincoli angolari soddisfatti; altrimenti 0 (fuori).
mask = (Epos & pOK & cond_ang).astype(float)

# --- Bordi analitici s23^{min/max}(s12) nel CM della coppia (1,2) ---
# Qui si passa nel CM del sottosistema (1,2) per ottenere una formula CHIUSA degli estremi di s23:
#   s23^{min/max}(s12) = m2^2 + m3^2 + 2 (E2* E3*  ∓  p2* p3*)
# dove gli asterischi indicano grandezze valutate nel CM di (1,2) e gli estremi corrispondono a cos = ±1
# Queste curve sono il "bordo teorico" esatto della regione fisica.
def s23_bounds_mev2(s12_array):
    s12 = np.asarray(s12_array)
    root = np.sqrt(s12)
    # energie e momenti in * del sistema (12)
    E2s = (s12 - m1**2 + m2**2) / (2*root)
    E3s = (s - s12 - m3**2) / (2*root)
    p2s = np.sqrt(np.clip(E2s**2 - m2**2, 0.0, None))
    p3s = np.sqrt(np.clip(E3s**2 - m3**2, 0.0, None))
    s23_min = m2**2 + m3**2 + 2*(E2s*E3s - p2s*p3s)  # cos = +1
    s23_max = m2**2 + m3**2 + 2*(E2s*E3s + p2s*p3s)  # cos = -1
    return s23_min, s23_max

s23_min, s23_max = s23_bounds_mev2(S12s)

# --- Plot ---
plt.figure(figsize=(8,6), dpi=150)

# Regione ammissibile (riempita)
# Mostra la zona in cui mask=1. Serve per visualizzare chiaramente l'area fisica.
plt.contourf(
    s12g/1e6, s23g, mask,
    levels=[0.5, 1.5],
    colors=["#cfe8ff"], alpha=0.9
)

# --- BORDO NUMERICO (dalla maschera) ---
# Perché disegnarlo?
# - È una VERIFICA INDIPENDENTE su griglia: dato solo il calcolo numerico dei vincoli (mask),
#   il contorno a livello 0.5 è il bordo "empirico" della regione fisica.
# - Confrontandolo col bordo analitico ci assicuriamo che la formula sia implementata correttamente
#   e/o che la risoluzione della griglia sia sufficiente.
plt.contour(
    s12g/1e6, s23g, mask,
    levels=[0.5],
    colors="#2b6cb0", linewidths=1.5, linestyles="--"
)

# --- BORDI ANALITICI ---
# Perché disegnarli?
# - Sono il "guscio" teorico esatto (dipende solo dalle masse), indipendente dalla griglia.
# - Se coincidono col bordo numerico, la nostra selezione di vincoli (energetici + geometrici) è consistente.
plt.plot(S12s/1e6, s23_min, label=r"$s_{23}^{\min}(s_{12})$",
         color="#ef6c00", linewidth=2.0)
plt.plot(S12s/1e6, s23_max, label=r"$s_{23}^{\max}(s_{12})$",
         color="#ef6c00", linewidth=2.0, linestyle=":")

plt.title(r"Dalitz plot $n\to p+e^-+\bar{\nu}_e$")
plt.xlabel(r"$s_{12}$ [GeV$^2$]")   # Nota: asse x in GeV^2 (divisione per 1e6 sopra)
plt.ylabel(r"$s_{23}$ [MeV$^2$]")   # Asse y in MeV^2; puoi uniformare in GeV^2 dividendo anche s23 per 1e6
plt.grid(alpha=0.25)

from matplotlib.patches import Patch
from matplotlib.lines import Line2D
legend_elems = [
    Patch(facecolor="#cfe8ff", edgecolor="#cfe8ff", label="regione ammissibile"),
    Line2D([0],[0], color="#2b6cb0", linestyle="--", lw=1.5, label="bordo (numerico)"),
    Line2D([0],[0], color="#ef6c00", lw=2.0, label=r"bordo analitico $s_{23}^{\min/\max}$"),
]
plt.legend(handles=legend_elems, loc="best")
plt.tight_layout()

# Salvataggio su file
plt.savefig("Dalitz_plot_neutron_beta_decay.png")
plt.show()

# --- Qualche numero utile ---
print(f"s = M^2 = {s/1e6:.9f} GeV^2")
print(f"Intervallo s12: [{S12s.min()/1e6:.9f}, {S12s.max()/1e6:.9f}] GeV^2")
print(f"s23 complessivo (MeV^2): [{np.min(s23_min):.6f}, {np.max(s23_max):.6f}]")
