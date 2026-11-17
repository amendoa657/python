"""
GABARITO 04 — Quartis, IQR e outliers (7 erros)

 #  Erro original                     Correção / explicação
 1  quantile(25)                      quantile(0.25)  -> pandas usa PROPORÇÃO (0 a 1). quantile(25) = ValueError
 2  np.percentile(cresc, 0.75)        np.percentile(cresc, 75) -> numpy usa PORCENTAGEM (0 a 100). Sem erro, mas valor errado!
 3  iqr = q1 - q3                     iqr = q3 - q1  (senão dá NEGATIVO)
 4  lim_inf = q1 - 1.5 * q1           lim_inf = q1 - 1.5 * iqr   (a regra usa o IQR nos DOIS limites)
 5  (< lim_inf) & (> lim_sup)         usar | (OU). Um número não pode ser menor que o inferior E maior que o superior ao mesmo tempo -> lista sempre vazia
 6  rótulos trocados: var x std       desvio padrão = .std() ; variância = .var()   (desvio = raiz da variância)
 7  assimetria invertida              média > mediana -> cauda à DIREITA (positiva); média < mediana -> ESQUERDA

Resumo para decorar:
   pandas  s.quantile(0.25)        numpy  np.percentile(x, 25)
   IQR = Q3 - Q1
   outlier se  x < Q1 - 1,5·IQR   OU   x > Q3 + 1,5·IQR
"""
import numpy as np
import pandas as pd

cresc = pd.Series([1.2, 0.8, 2.5, 1.9, -1.5, 1.1, 2.3, 6.8, 1.4, 1.0, 1.8, 2.4])

q1 = cresc.quantile(0.25)                       # CORRIGIDO (1)
q2 = cresc.quantile(0.50)
q3 = np.percentile(cresc, 75)                   # CORRIGIDO (2)
iqr = q3 - q1                                   # CORRIGIDO (3)
print(f"Q1={q1:.2f}  Q2={q2}  Q3={q3:.2f}  IQR={iqr:.2f}")

lim_inf = q1 - 1.5 * iqr                        # CORRIGIDO (4)
lim_sup = q3 + 1.5 * iqr
print(f"Limites: {lim_inf:.2f} a {lim_sup:.2f}")

outliers = cresc[(cresc < lim_inf) | (cresc > lim_sup)]   # CORRIGIDO (5)
print("Outliers:", outliers.tolist())

print(f"Desvio padrão (amostral): {cresc.std():.2f}")     # CORRIGIDO (6)
print(f"Variância (amostral): {cresc.var():.2f}")

media, mediana = cresc.mean(), cresc.median()
print(f"Média={media:.2f}  Mediana={mediana:.2f}")
if media > mediana:
    print("Conclusão: média > mediana -> assimetria à DIREITA")      # CORRIGIDO (7)
else:
    print("Conclusão: média <= mediana -> assimetria à ESQUERDA ou simétrica")
