"""
gerar_dados.py — cria as bases de exemplo usadas no projeto de estudo.

ATENÇÃO: os números aqui são FICTÍCIOS, mas imitam o formato e a ordem de
grandeza das tabelas reais do IBGE (SIDRA / PNAD Contínua). Servem só para
treinar. Na prova/trabalho real, você baixaria a tabela do SIDRA
(https://sidra.ibge.gov.br) ou receberia o arquivo do professor.

Como rodar:   python dados/gerar_dados.py
Ele cria 3 arquivos dentro da pasta dados/:
  1. afazeres_domesticos.csv      -> base LIMPA (pronta para usar)
  2. afazeres_domesticos_sujo.csv -> a mesma base, mas "suja" como vem do IBGE
                                      (serve para treinar ETL/limpeza)
  3. desocupacao_uf.csv           -> taxa de desemprego por UF, 2012 x 2022
"""

import numpy as np      # NumPy: números e sorteios aleatórios
import pandas as pd     # Pandas: tabelas (DataFrames)
from pathlib import Path

# "Semente" do gerador aleatório: com a mesma semente, os números sorteados
# são SEMPRE os mesmos. Assim todo mundo que rodar o script terá a mesma base.
rng = np.random.default_rng(42)

PASTA = Path(__file__).parent  # pasta onde este arquivo está (dados/)

# ---------------------------------------------------------------------------
# Tabela auxiliar: UF -> Região
# ---------------------------------------------------------------------------
REGIOES = {
    "AC": "Norte", "AM": "Norte", "AP": "Norte", "PA": "Norte", "RO": "Norte",
    "RR": "Norte", "TO": "Norte",
    "AL": "Nordeste", "BA": "Nordeste", "CE": "Nordeste", "MA": "Nordeste",
    "PB": "Nordeste", "PE": "Nordeste", "PI": "Nordeste", "RN": "Nordeste",
    "SE": "Nordeste",
    "DF": "Centro-Oeste", "GO": "Centro-Oeste", "MS": "Centro-Oeste",
    "MT": "Centro-Oeste",
    "ES": "Sudeste", "MG": "Sudeste", "RJ": "Sudeste", "SP": "Sudeste",
    "PR": "Sul", "RS": "Sul", "SC": "Sul",
}

# ---------------------------------------------------------------------------
# 1) AFAZERES DOMÉSTICOS (horas semanais em cuidados/afazeres)
#    Formato "longo": cada linha = 1 combinação de UF/ano/sexo/raça/...
# ---------------------------------------------------------------------------
linhas = []
for uf, regiao in REGIOES.items():
    # cada estado tem um "efeito" próprio (uns um pouco acima, outros abaixo)
    efeito_uf = rng.normal(0, 1.2)
    for ano in [2016, 2017, 2018, 2019, 2022]:
        for sexo in ["Mulheres", "Homens"]:
            for raca in ["Branca", "Preta ou parda"]:
                for faixa in ["14 a 24 anos", "25 a 49 anos", "50 anos ou mais"]:
                    for condicao in ["Ocupada", "Desocupada"]:
                        # valores-base parecidos com a realidade brasileira:
                        # mulheres ~21h/semana, homens ~11h/semana
                        base = 21.5 if sexo == "Mulheres" else 11.0
                        if raca == "Preta ou parda" and sexo == "Mulheres":
                            base += 1.5          # mulheres negras: mais horas
                        if faixa == "50 anos ou mais":
                            base += 1.0
                        if faixa == "14 a 24 anos":
                            base -= 3.0
                        if condicao == "Desocupada":
                            base += 3.5 if sexo == "Mulheres" else 1.5
                        # pequena tendência de queda da diferença ao longo dos anos
                        tendencia = -(ano - 2016) * (0.12 if sexo == "Mulheres" else -0.08)
                        horas = base + efeito_uf + tendencia + rng.normal(0, 1.0)
                        linhas.append([uf, regiao, ano, sexo, raca, faixa,
                                       condicao, round(horas, 1)])

df = pd.DataFrame(linhas, columns=["uf", "regiao", "ano", "sexo", "raca",
                                   "faixa_etaria", "condicao", "horas_semanais"])

# Plantamos 2 OUTLIERS de propósito (valores absurdos) para treinar a detecção.
df.loc[5, "horas_semanais"] = 48.0     # alto demais
df.loc[777, "horas_semanais"] = 1.2    # baixo demais

df.to_csv(PASTA / "afazeres_domesticos.csv", index=False)
print("OK afazeres_domesticos.csv ->", df.shape, "(linhas, colunas)")

# ---------------------------------------------------------------------------
# 2) A MESMA BASE, MAS "SUJA" — do jeito que costuma vir do SIDRA/Excel
#    Problemas inseridos (todos aparecem em prova!):
#      - separador ";" e vírgula decimal ("21,5")
#      - acentos com encoding latin-1
#      - linhas de título/notas antes do cabeçalho
#      - nomes de colunas com espaço e maiúsculas
#      - "..." e "-" no lugar de números (padrão IBGE para "sem dado")
#      - espaços sobrando e letras trocadas (" ba", "Ba")
#      - linhas duplicadas
# ---------------------------------------------------------------------------
sujo = df.sample(400, random_state=1).copy()
sujo.columns = ["Unidade da Federação", "Região", "Ano", "Sexo", "Cor ou raça",
                "Grupo de idade", "Condição de ocupação", "Horas semanais"]
sujo["Horas semanais"] = sujo["Horas semanais"].astype(str).str.replace(".", ",", regex=False)
sujo.iloc[3, 7] = "..."           # sem dado
sujo.iloc[10, 7] = "-"            # IBGE usa "-" para zero/inexistente
sujo.iloc[20, 7] = ""             # célula vazia
sujo.iloc[7, 0] = " ba"           # espaço + minúscula
sujo.iloc[8, 0] = "Pe "
sujo.iloc[9, 3] = "mulheres"
sujo = pd.concat([sujo, sujo.iloc[:5]])   # 5 linhas duplicadas

caminho_sujo = PASTA / "afazeres_domesticos_sujo.csv"
with open(caminho_sujo, "w", encoding="latin-1", newline="") as f:
    f.write("Tabela 1.1 - Horas semanais dedicadas a afazeres domésticos (FICTÍCIO)\n")
    f.write("Fonte: dados simulados para estudo\n")
    sujo.to_csv(f, sep=";", index=False)
print("OK afazeres_domesticos_sujo.csv ->", sujo.shape)

# ---------------------------------------------------------------------------
# 3) DESOCUPAÇÃO (desemprego) por UF e sexo, 2012 x 2022 — formato "largo"
# ---------------------------------------------------------------------------
lin = []
for uf, regiao in REGIOES.items():
    base2012 = rng.uniform(5, 11) + (2 if regiao == "Nordeste" else 0)
    base2022 = base2012 + rng.normal(0.5, 1.8)
    for sexo, extra in [("Homens", -1.2), ("Mulheres", 1.8)]:
        lin.append([uf, regiao, sexo,
                    round(base2012 + extra + rng.normal(0, .4), 1),
                    round(base2022 + extra + rng.normal(0, .4), 1)])
deso = pd.DataFrame(lin, columns=["uf", "regiao", "sexo", "taxa_2012", "taxa_2022"])
deso.to_csv(PASTA / "desocupacao_uf.csv", index=False)
print("OK desocupacao_uf.csv ->", deso.shape)
