"""
EXERCÍCIO 03 — Pandas / ETL da base "suja" do IBGE        (8 erros)
-----------------------------------------------------------------
Objetivo: ler dados/afazeres_domesticos_sujo.csv, limpar e responder:
  "Qual a média de horas de mulheres e homens nos estados BA, PE e CE em 2022?"

Sobre o arquivo (abra no bloco de notas para ver!):
  - tem 2 linhas de título antes do cabeçalho
  - separador é ";"   e a casa decimal é ","
  - acentos em latin-1
  - "..." e "-" significam "sem dado"
  - a coluna de UF tem espaços e minúsculas (" ba", "Pe ")
  - tem linhas duplicadas

Saída esperada (aprox.):  uma tabela com Homens 14.2 e Mulheres 24.3,
e a mensagem "Linhas após limpeza: 397".

Rode a partir da pasta do projeto:  python exercicios_corrigir/ex03_pandas_etl.py
Gabarito: exercicios_corrigir/gabarito/ex03_pandas_etl.py
"""
import pandas as pd

df = pd.read_csv("dados/afazeres_domesticos_sujo.csv")

df = df.rename(columns={
    "Unidade da Federação": "uf",
    "Ano": "ano",
    "Sexo": "sexo",
    "Horas semanais": "horas",
})

df["uf"] = df["uf"].str.strip()
df["sexo"] = df["sexo"].str.strip().str.capitalize()

df.dropna(subset=["horas"])
df = df.drop_duplicates()
print("Linhas após limpeza:", len(df))

filtro = df[df["uf"].isin("BA", "PE", "CE") and df["ano"] = 2022]

resultado = filtro.groupby("Sexo")["horas"].mean
print(resultado.round(1))
