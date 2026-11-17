"""
=============================================================================
AULA 03 — ESTATÍSTICA DESCRITIVA (média, mediana, moda, quartis, IQR,
          amplitude, variância, desvio padrão e OUTLIERS)
=============================================================================
Como rodar:  python aulas/03_estatistica.py

Estratégia desta aula: para cada medida você vê
   (1) o CONCEITO,  (2) a CONTA NA MÃO,  (3) o CÓDIGO em Python puro,
   (4) o CÓDIGO com Pandas/NumPy,  (5) COMO INTERPRETAR para a persona.

Vamos usar um exemplo pequeno (dá para conferir na calculadora):
   Taxa de desemprego (%) de 9 estados fictícios:
       [6, 7, 7, 8, 9, 10, 11, 12, 30]
   (o 30 é um OUTLIER de propósito)
=============================================================================
"""
import numpy as np
import pandas as pd
from pathlib import Path

dados = [6, 7, 7, 8, 9, 10, 11, 12, 30]
s = pd.Series(dados)   # a mesma lista como Series do Pandas
n = len(dados)

print("Dados:", dados, "| n =", n)

# ===========================================================================
# 1. MÉDIA ARITMÉTICA  (tendência central)
# ===========================================================================
# Conceito: soma tudo e divide pela quantidade.
#   média = (6+7+7+8+9+10+11+12+30) / 9 = 100 / 9 = 11,11
# Interpretação: é o valor "se todo mundo fosse igual". É SENSÍVEL a outliers:
#   aquele 30 puxa a média para cima.
media_manual = sum(dados) / n
media_pd = s.mean()
media_np = np.mean(dados)
print(f"\n1) MÉDIA      manual={media_manual:.2f}  pandas={media_pd:.2f}  numpy={media_np:.2f}")

# ===========================================================================
# 2. MEDIANA  (tendência central, ROBUSTA)
# ===========================================================================
# Conceito: ORDENA os dados e pega o valor do MEIO.
#   - n ímpar: o elemento da posição (n+1)/2.   Aqui n=9 -> 5ª posição = 9
#   - n par:   média dos DOIS do meio. Ex.: [1,2,3,4] -> (2+3)/2 = 2,5
# Interpretação: metade dos estados está abaixo de 9% e metade acima.
#   NÃO é afetada pelo outlier 30 (se fosse 300, a mediana continuaria 9).
def mediana_manual(valores):
    v = sorted(valores)           # 1º passo SEMPRE: ordenar!
    meio = len(v) // 2
    if len(v) % 2 == 1:           # ímpar
        return v[meio]
    return (v[meio - 1] + v[meio]) / 2   # par

print(f"2) MEDIANA    manual={mediana_manual(dados)}  pandas={s.median()}  numpy={np.median(dados)}")

# ===========================================================================
# 3. MODA
# ===========================================================================
# Conceito: valor que MAIS se repete. Aqui: 7 (aparece 2x).
#   Pode não existir (todos diferentes) ou ter várias (bimodal).
#   Útil para dados categóricos: "qual o meio de transporte mais usado?"
contagem = {}
for v in dados:
    contagem[v] = contagem.get(v, 0) + 1
moda_manual = max(contagem, key=contagem.get)
print(f"3) MODA       manual={moda_manual}  pandas={s.mode().tolist()}")
# ATENÇÃO: s.mode() devolve uma Series (pode haver mais de uma moda). Use s.mode()[0] para pegar a 1ª.

# ===========================================================================
# 4. AMPLITUDE  (dispersão mais simples)
# ===========================================================================
# Conceito: máximo - mínimo = 30 - 6 = 24
# Interpretação: distância entre o "melhor" e o "pior" estado. Muito afetada por outlier.
print(f"4) AMPLITUDE  {max(dados) - min(dados)}  pandas={s.max() - s.min()}")

# ===========================================================================
# 5. VARIÂNCIA e DESVIO PADRÃO  (dispersão em torno da média)
# ===========================================================================
# Conceito:
#   1) calcula a distância de cada valor até a média  (x - média)
#   2) eleva ao quadrado (para negativo não cancelar positivo)
#   3) soma tudo
#   4) divide por n (POPULACIONAL) ou por n-1 (AMOSTRAL)   -> isso é a VARIÂNCIA
#   5) tira a RAIZ QUADRADA                                 -> DESVIO PADRÃO
#
#   Variância está em "unidade ao quadrado" (%²) — difícil de interpretar.
#   Desvio padrão volta para a unidade original (%) — é o que se interpreta!
#   NÃO CONFUNDA os dois (a rubrica cita esse erro explicitamente!).
#
# Interpretação: "em média, os estados se afastam ~X pontos da média".
#   Desvio pequeno = estados HOMOGÊNEOS (parecidos). Grande = HETEROGÊNEOS (desiguais).
desvios_quadrado = [(x - media_manual) ** 2 for x in dados]
var_pop = sum(desvios_quadrado) / n          # divide por n
var_amostral = sum(desvios_quadrado) / (n - 1)  # divide por n-1
dp_pop = var_pop ** 0.5
dp_amostral = var_amostral ** 0.5
print(f"5) VARIÂNCIA  populacional={var_pop:.2f}  amostral={var_amostral:.2f}")
print(f"   DESVIO P.  populacional={dp_pop:.2f}  amostral={dp_amostral:.2f}")

# !!!!! PEGADINHA FAMOSA (cai em "corrigir código") !!!!!
#   Pandas  s.std()   -> AMOSTRAL por padrão (ddof=1, divide por n-1)
#   NumPy   np.std()  -> POPULACIONAL por padrão (ddof=0, divide por n)
#   Por isso os dois dão números DIFERENTES para os mesmos dados.
#   Para igualar: s.std(ddof=0) == np.std(dados)   ou   np.std(dados, ddof=1) == s.std()
print(f"   pandas s.std()={s.std():.2f} (amostral) | numpy np.std()={np.std(dados):.2f} (populacional)")
print(f"   pandas s.std(ddof=0)={s.std(ddof=0):.2f} | numpy np.std(ddof=1)={np.std(dados, ddof=1):.2f}")
print(f"   variância pandas s.var()={s.var():.2f}  (lembrete: desvio = raiz da variância)")
# Qual usar? Dados de TODOS os estados (27 UFs) = população -> ddof=0 é defensável.
# Mas o padrão do Pandas (ddof=1) é o mais usado em trabalhos. O importante é saber explicar.

# Coeficiente de variação (bônus): desvio / média * 100 -> dispersão em %.
#   Permite comparar a dispersão de coisas com escalas diferentes. CV > 30% = alta dispersão.
print(f"   CV = {s.std() / s.mean() * 100:.1f}%")

# ===========================================================================
# 6. QUARTIS (Q1, Q2, Q3) e IQR (intervalo interquartil)
# ===========================================================================
# Conceito: dividem os dados ORDENADOS em 4 partes com 25% cada.
#   Q1 = 25% dos dados estão abaixo dele
#   Q2 = 50% -> É A MEDIANA
#   Q3 = 75% dos dados estão abaixo dele
#   IQR = Q3 - Q1 -> tamanho da "metade do meio" dos dados (os 50% centrais)
#
# Conta na mão (método do Pandas/NumPy, "interpolação linear"):
#   posição = (n - 1) * p   (contando do índice 0)
#   ordenados: idx 0:6  1:7  2:7  3:8  4:9  5:10  6:11  7:12  8:30
#   Q1: (9-1)*0.25 = 2  -> valor no índice 2 = 7
#   Q2: (9-1)*0.50 = 4  -> índice 4 = 9
#   Q3: (9-1)*0.75 = 6  -> índice 6 = 11
#   Se a posição der quebrada (ex.: 2.5), faz a média ponderada entre os vizinhos.
#   IQR = 11 - 7 = 4
#
# OBS: existe o "método escolar" (mediana da metade inferior/superior) que pode dar
#   valores um pouco diferentes. Ambos estão certos — são convenções diferentes.
q1 = s.quantile(0.25)
q2 = s.quantile(0.50)
q3 = s.quantile(0.75)
iqr = q3 - q1
print(f"6) QUARTIS    Q1={q1}  Q2={q2} (=mediana)  Q3={q3}  ->  IQR = Q3 - Q1 = {iqr}")
print(f"   numpy: {np.percentile(dados, [25, 50, 75])}")
# ERROS COMUNS: quantile(25) em vez de quantile(0.25)  -> ValueError (tem que ser entre 0 e 1)
#               np.percentile(dados, 0.25) -> errado! numpy usa 0–100: np.percentile(dados, 25)
#               IQR = Q1 - Q3 (invertido, dá negativo)

# ===========================================================================
# 7. OUTLIERS — REGRA DO 1,5 × IQR  (método de Tukey, o do boxplot)
# ===========================================================================
# Limite inferior = Q1 - 1,5 × IQR = 7 - 1,5×4 = 7 - 6 = 1
# Limite superior = Q3 + 1,5 × IQR = 11 + 6 = 17
# Qualquer valor < 1 ou > 17 é OUTLIER -> o 30 é outlier!
lim_inf = q1 - 1.5 * iqr
lim_sup = q3 + 1.5 * iqr
outliers = s[(s < lim_inf) | (s > lim_sup)]
print(f"7) OUTLIERS   limites [{lim_inf}, {lim_sup}]  ->  outliers: {outliers.tolist()}")

# EFEITO DO OUTLIER NA MÉDIA x MEDIANA (pergunta CERTA de prova/apresentação):
sem_outlier = s[(s >= lim_inf) & (s <= lim_sup)]
print(f"   Com outlier:  média={s.mean():.2f}  mediana={s.median():.2f}")
print(f"   Sem outlier:  média={sem_outlier.mean():.2f}  mediana={sem_outlier.median():.2f}")
print("   -> A média caiu bastante; a mediana quase não mudou. Por isso, com outliers,")
print("      a MEDIANA representa melhor o 'estado típico'.")

# ===========================================================================
# 8. ASSIMETRIA (comparando média e mediana)
# ===========================================================================
#   média > mediana  -> assimetria POSITIVA (à direita): cauda de valores ALTOS
#                       (típico de RENDA: poucos muito ricos puxam a média)
#   média < mediana  -> assimetria NEGATIVA (à esquerda): cauda de valores BAIXOS
#   média ≈ mediana  -> distribuição aproximadamente SIMÉTRICA
def tipo_assimetria(serie):
    m, md = serie.mean(), serie.median()
    if abs(m - md) < 0.05 * serie.std():
        return "aproximadamente simétrica"
    return "assimétrica à DIREITA (positiva)" if m > md else "assimétrica à ESQUERDA (negativa)"

print(f"8) ASSIMETRIA {tipo_assimetria(s)}  | pandas skew={s.skew():.2f} (>0 = direita)")

# ===========================================================================
# 9. TUDO DE UMA VEZ — função reaproveitável (use no dashboard!)
# ===========================================================================
def resumo_estatistico(serie):
    """Devolve um dicionário com TODAS as medidas exigidas no trabalho."""
    serie = serie.dropna()                 # remove NaN antes (senão algumas contas dão NaN)
    q1, q3 = serie.quantile(0.25), serie.quantile(0.75)
    iqr = q3 - q1
    li, ls = q1 - 1.5 * iqr, q3 + 1.5 * iqr
    return {
        "n": int(serie.count()),
        "media": serie.mean(),
        "mediana": serie.median(),
        "moda": serie.mode().iloc[0] if not serie.mode().empty else None,
        "minimo": serie.min(),
        "maximo": serie.max(),
        "amplitude": serie.max() - serie.min(),
        "variancia": serie.var(),
        "desvio_padrao": serie.std(),
        "q1": q1, "q2": serie.median(), "q3": q3,
        "iqr": iqr,
        "limite_inferior": li, "limite_superior": ls,
        "qtd_outliers": int(((serie < li) | (serie > ls)).sum()),
    }

print("\n9) Resumo do exemplo:")
for k, v in resumo_estatistico(s).items():
    print(f"   {k:16s} {v:.2f}" if isinstance(v, float) else f"   {k:16s} {v}")

# describe() já dá quase tudo (count, mean, std, min, 25%, 50%, 75%, max):
print(s.describe())

# ===========================================================================
# 10. APLICANDO NA BASE DO IBGE (afazeres domésticos)
# ===========================================================================
print("\n" + "=" * 70, "\n10) Aplicando na base de afazeres domésticos\n" + "=" * 70)
df = pd.read_csv(Path(__file__).parent.parent / "dados" / "afazeres_domesticos.csv")

r = resumo_estatistico(df["horas_semanais"])
print(f"Geral: média={r['media']:.1f}h  mediana={r['mediana']:.1f}h  DP={r['desvio_padrao']:.1f}h  "
      f"IQR={r['iqr']:.1f}h  outliers={r['qtd_outliers']}")

# Estatísticas por grupo (para comparar homens x mulheres)
tabela = df.groupby("sexo")["horas_semanais"].agg(
    media="mean", mediana="median", desvio="std",
    q1=lambda x: x.quantile(0.25), q3=lambda x: x.quantile(0.75))
tabela["iqr"] = tabela["q3"] - tabela["q1"]
print(tabela.round(2))

# Discrepância média entre homens e mulheres (pergunta de negócio da persona 1)
m = df.groupby("sexo")["horas_semanais"].mean()
print(f"\nMulheres dedicam em média {m['Mulheres'] - m['Homens']:.1f}h a MAIS por semana que homens "
      f"({m['Mulheres'] / m['Homens']:.1f}x mais).")

# Outliers na base real: QUAIS linhas são?
q1, q3 = df["horas_semanais"].quantile([0.25, 0.75])
iqr = q3 - q1
mask = (df["horas_semanais"] < q1 - 1.5 * iqr) | (df["horas_semanais"] > q3 + 1.5 * iqr)
print("\nOutliers encontrados (regra 1,5×IQR, base inteira):")
print(df.loc[mask, ["uf", "ano", "sexo", "raca", "horas_semanais"]])
# DICA: calcular outlier DENTRO de cada grupo costuma fazer mais sentido
# (homens e mulheres têm distribuições diferentes):
def marca_outlier(x):
    a, b = x.quantile([0.25, 0.75])
    return (x < a - 1.5 * (b - a)) | (x > b + 1.5 * (b - a))
df["outlier_no_grupo"] = df.groupby("sexo")["horas_semanais"].transform(marca_outlier)
print("Outliers calculados dentro de cada sexo:", int(df["outlier_no_grupo"].sum()))

print("""
=============================================================================
COMO FALAR ISSO NA APRESENTAÇÃO / PROVA DISCURSIVA (modelo de frase):
  "A mediana de horas das mulheres é X h, contra Y h dos homens — uma
   diferença de Z h por semana. O desvio padrão de D h mostra que os estados
   são [homogêneos/heterogêneos]. Identificamos N outliers pela regra
   1,5×IQR; por isso recomendamos usar a MEDIANA como referência, já que a
   média é puxada por esses valores extremos."
=============================================================================
""")
