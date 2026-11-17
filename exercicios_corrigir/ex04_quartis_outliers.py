"""
EXERCÍCIO 04 — Quartis, IQR, desvio padrão e outliers        (7 erros)
-----------------------------------------------------------------
Taxa de crescimento populacional (%) de 12 capitais (fictício):

Saída esperada:
    Q1=1.08  Q2=1.6  Q3=2.32  IQR=1.25
    Limites: -0.80 a 4.20
    Outliers: [-1.5, 6.8]
    Desvio padrão (amostral): 1.90
    Variância (amostral): 3.60
    Média=1.81  Mediana=1.60
    Conclusão: média > mediana -> assimetria à DIREITA

Gabarito: exercicios_corrigir/gabarito/ex04_quartis_outliers.py
"""
import numpy as np
import pandas as pd

cresc = pd.Series([1.2, 0.8, 2.5, 1.9, -1.5, 1.1, 2.3, 6.8, 1.4, 1.0, 1.8, 2.4])

q1 = cresc.quantile(25)
q2 = cresc.quantile(0.50)
q3 = np.percentile(cresc, 0.75)
iqr = q1 - q3
print(f"Q1={q1:.2f}  Q2={q2}  Q3={q3:.2f}  IQR={iqr:.2f}")

lim_inf = q1 - 1.5 * q1
lim_sup = q3 + 1.5 * iqr
print(f"Limites: {lim_inf:.2f} a {lim_sup:.2f}")

outliers = cresc[(cresc < lim_inf) & (cresc > lim_sup)]
print("Outliers:", outliers.tolist())

print(f"Desvio padrão (amostral): {cresc.var():.2f}")
print(f"Variância (amostral): {cresc.std():.2f}")

media, mediana = cresc.mean(), cresc.median()
print(f"Média={media:.2f}  Mediana={mediana:.2f}")
if media > mediana:
    print("Conclusão: média > mediana -> assimetria à ESQUERDA")
else:
    print("Conclusão: média <= mediana -> assimetria à DIREITA")
