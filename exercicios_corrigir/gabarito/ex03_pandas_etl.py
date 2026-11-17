"""
GABARITO 03 — Pandas / ETL (8 erros)

 #  Erro original                                  Sintoma                       Correção
 1  read_csv sem sep/decimal/encoding/skiprows     UnicodeDecodeError/ParserError sep=";", decimal=",", encoding="latin-1", skiprows=2
 2  sem na_values                                  coluna "horas" vira texto     na_values=["...", "-"]
 3  .str.strip() sem .str.upper() na UF            " ba" vira "ba" (não casa "BA") .str.strip().str.upper()
 4  df.dropna(...) sem atribuir                    NaN continua lá (sem erro!)    df = df.dropna(...)
 5  .isin("BA", "PE", "CE")                         TypeError                     .isin(["BA", "PE", "CE"])  <- LISTA
 6  "and" entre condições do pandas                 ValueError: truth value ambiguous  usar "&" e PARÊNTESES
 7  df["ano"] = 2022 dentro do filtro               SyntaxError                   == (comparação)
 8  groupby("Sexo") e .mean sem ()                  KeyError / mostra "<bound method>" groupby("sexo") e .mean()

LIÇÕES:
  * Métodos do pandas (dropna, drop_duplicates, rename, fillna, sort_values...)
    DEVOLVEM uma tabela nova. Se não atribuir (df = ...), nada muda.
  * Nome de coluna é case-sensitive: "Sexo" != "sexo" -> KeyError.
  * Método sem parênteses não executa: df.mean é a função; df.mean() é o resultado.
"""
import pandas as pd

df = pd.read_csv(
    "dados/afazeres_domesticos_sujo.csv",
    sep=";", decimal=",", encoding="latin-1", skiprows=2,   # CORRIGIDO (1)
    na_values=["...", "-"],                                  # CORRIGIDO (2)
)

df = df.rename(columns={
    "Unidade da Federação": "uf",
    "Ano": "ano",
    "Sexo": "sexo",
    "Horas semanais": "horas",
})

df["uf"] = df["uf"].str.strip().str.upper()                  # CORRIGIDO (3)
df["sexo"] = df["sexo"].str.strip().str.capitalize()

df = df.dropna(subset=["horas"])                             # CORRIGIDO (4)
df = df.drop_duplicates()
print("Linhas após limpeza:", len(df))

filtro = df[(df["uf"].isin(["BA", "PE", "CE"])) & (df["ano"] == 2022)]   # CORRIGIDO (5)(6)(7)

resultado = filtro.groupby("sexo")["horas"].mean()           # CORRIGIDO (8)
print(resultado.round(1))
