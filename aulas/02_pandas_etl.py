"""
=============================================================================
AULA 02 — PANDAS E ETL (carregar, limpar e filtrar dados do IBGE)
=============================================================================
Como rodar (a partir da pasta do projeto):  python aulas/02_pandas_etl.py

O QUE É ETL?
  E = Extract   (Extrair)   -> ler o arquivo CSV/XLSX ou baixar da API
  T = Transform (Transformar)-> limpar: nomes de colunas, tipos, vazios,
                               duplicados, padronizar textos, criar colunas
  L = Load      (Carregar)  -> salvar a base limpa / usar no dashboard

O QUE É PANDAS?
  Biblioteca para trabalhar com TABELAS. A tabela se chama DataFrame (df).
  Cada coluna de um DataFrame é uma Series.
     df["horas"]      -> uma Series (1 coluna)
     df[["uf","ano"]] -> um DataFrame (várias colunas -> COLCHETE DUPLO!)
=============================================================================
"""
import numpy as np
import pandas as pd
from pathlib import Path

PASTA_DADOS = Path(__file__).parent.parent / "dados"

# ===========================================================================
# PARTE A — EXTRACT: LER ARQUIVOS
# ===========================================================================
print("=" * 70, "\nPARTE A — Ler a base LIMPA\n" + "=" * 70)

df = pd.read_csv(PASTA_DADOS / "afazeres_domesticos.csv")
#   Para Excel:  pd.read_excel("arquivo.xlsx", sheet_name=0)   (precisa do openpyxl)

# Primeira coisa a fazer SEMPRE: olhar a cara dos dados
print(df.head())          # 5 primeiras linhas   (df.tail() = 5 últimas)
print(df.shape)           # (linhas, colunas)  -> atributo, SEM parênteses!
print(df.columns.tolist())  # nomes das colunas
print(df.dtypes)          # tipo de cada coluna (int64, float64, object/str)
df.info()                 # resumo: tipos + quantos valores não-nulos
print(df.describe())      # estatísticas rápidas das colunas numéricas

# ===========================================================================
# PARTE B — SELECIONAR E FILTRAR
# ===========================================================================
print("\n" + "=" * 70, "\nPARTE B — Selecionar e filtrar\n" + "=" * 70)

# Selecionar colunas
print(df["horas_semanais"].head(3))         # 1 coluna  -> Series
print(df[["uf", "sexo", "horas_semanais"]].head(3))  # várias -> lista dentro []

# Filtrar linhas com condição (máscara booleana)
so_bahia = df[df["uf"] == "BA"]
print("Linhas da Bahia:", len(so_bahia))

# Várias condições: use  &  (E)  |  (OU)  ~ (NÃO)  e PARÊNTESES em cada condição
#   ERRADO: df[df["uf"] == "BA" and df["ano"] == 2022]   -> ValueError (ambiguous)
#   ERRADO: df[df["uf"] == "BA" & df["ano"] == 2022]     -> erro de precedência
#   CERTO:
ba_2022 = df[(df["uf"] == "BA") & (df["ano"] == 2022)]
print("Bahia em 2022:", len(ba_2022))

# Filtro por LISTA de valores -> .isin()   (é isso que o multiselect do Streamlit usa)
estados = ["BA", "PE", "AM", "CE"]
df_personas = df[df["uf"].isin(estados)]
print("Estados das personas:", df_personas["uf"].unique())

# Filtro por intervalo -> .between(inicio, fim)   (o slider do Streamlit usa)
recentes = df[df["ano"].between(2018, 2022)]
print("Anos 2018–2022:", sorted(recentes["ano"].unique()))

# .loc[linhas, colunas]  -> por RÓTULO/condição
print(df.loc[df["horas_semanais"] > 30, ["uf", "horas_semanais"]].head())
# .iloc[linhas, colunas] -> por POSIÇÃO (números)
print(df.iloc[0:3, 0:4])

# ===========================================================================
# PARTE C — AGRUPAR (groupby) — responde as "perguntas de negócio"
# ===========================================================================
print("\n" + "=" * 70, "\nPARTE C — groupby\n" + "=" * 70)

# "Qual a média de horas por sexo?"
print(df.groupby("sexo")["horas_semanais"].mean())

# "Média por estado E sexo" -> agrupa por 2 colunas
media_uf_sexo = df.groupby(["uf", "sexo"])["horas_semanais"].mean().reset_index()
print(media_uf_sexo.head())
# .reset_index() transforma o resultado de volta em tabela "normal" (bom p/ gráficos)

# Várias estatísticas de uma vez -> .agg()
resumo = df.groupby("regiao")["horas_semanais"].agg(["mean", "median", "std", "count"])
print(resumo.round(2))

# Pivot: transforma linhas em colunas (formato "largo")
pivo = df.pivot_table(index="uf", columns="sexo", values="horas_semanais", aggfunc="mean")
pivo["diferenca"] = pivo["Mulheres"] - pivo["Homens"]   # criar coluna nova!
print(pivo.sort_values("diferenca", ascending=False).head().round(1))

# Ordenar
print(media_uf_sexo.sort_values("horas_semanais", ascending=False).head(3))

# Contar categorias
print(df["regiao"].value_counts())

# ===========================================================================
# PARTE D — TRANSFORM: LIMPAR UMA BASE "SUJA" (do jeito que vem do IBGE)
# ===========================================================================
print("\n" + "=" * 70, "\nPARTE D — ETL da base SUJA\n" + "=" * 70)

# Problemas típicos de arquivos do IBGE/SIDRA:
#  1) separador ";" em vez de ","      -> sep=";"
#  2) vírgula decimal "21,5"           -> decimal=","
#  3) acentos quebrados (Ã§, Ã£)       -> encoding="latin-1" (ou "utf-8", "cp1252")
#  4) linhas de título antes do cabeçalho -> skiprows=N
#  5) "...", "-", "X" no lugar de número -> na_values=[...]
#  6) espaços, maiúsculas/minúsculas misturadas
#  7) linhas duplicadas

# Se tentar ler "do jeito normal", dá ruim:
try:
    pd.read_csv(PASTA_DADOS / "afazeres_domesticos_sujo.csv")
except Exception as erro:
    print("Leitura ingênua falhou:", type(erro).__name__)

# Leitura CORRETA:
sujo = pd.read_csv(
    PASTA_DADOS / "afazeres_domesticos_sujo.csv",
    sep=";",                    # separador de colunas
    decimal=",",                # vírgula é a casa decimal
    encoding="latin-1",         # codificação dos acentos
    skiprows=2,                 # pula as 2 linhas de título
    na_values=["...", "-", "X", ""],  # tudo isso vira NaN (valor ausente)
)
print(sujo.head())
print("Tipo da coluna de horas:", sujo["Horas semanais"].dtype)  # float64 = deu certo

# --- D1. Renomear colunas para nomes simples (sem espaço/acento) ---
sujo = sujo.rename(columns={
    "Unidade da Federação": "uf",
    "Região": "regiao",
    "Ano": "ano",
    "Sexo": "sexo",
    "Cor ou raça": "raca",
    "Grupo de idade": "faixa_etaria",
    "Condição de ocupação": "condicao",
    "Horas semanais": "horas_semanais",
})
# Alternativa genérica:  df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

# --- D2. Padronizar textos ---
sujo["uf"] = sujo["uf"].str.strip().str.upper()       # " ba" -> "BA"
sujo["sexo"] = sujo["sexo"].str.strip().str.capitalize()  # "mulheres" -> "Mulheres"

# --- D3. Valores ausentes (NaN) ---
print("Nulos por coluna:\n", sujo.isna().sum())
# Opção 1: remover as linhas sem o valor principal
sujo = sujo.dropna(subset=["horas_semanais"])
# Opção 2 (alternativa): preencher -> sujo["horas_semanais"].fillna(sujo["horas_semanais"].median())
#   Preencher com a MEDIANA é mais seguro que com a média (a mediana não é puxada por outliers).

# --- D4. Duplicados ---
print("Duplicados:", sujo.duplicated().sum())
sujo = sujo.drop_duplicates()

# --- D5. Garantir tipos ---
sujo["ano"] = sujo["ano"].astype(int)
# Se a coluna numérica veio como texto "21,5" (porque esqueceu decimal=","):
#   df["col"] = pd.to_numeric(df["col"].str.replace(",", "."), errors="coerce")
#   errors="coerce" -> o que não der para converter vira NaN em vez de dar erro.

# --- D6. Criar colunas novas (feature) ---
sujo["acima_de_20h"] = sujo["horas_semanais"] > 20
sujo["grupo"] = sujo["sexo"] + " " + sujo["raca"]   # ex.: "Mulheres Preta ou parda"
# Mapear valores com um dicionário:
sujo["sexo_sigla"] = sujo["sexo"].map({"Mulheres": "F", "Homens": "M"})

print("\nBase limpa:")
print(sujo.head())
print("Formato final:", sujo.shape)

# ===========================================================================
# PARTE E — LOAD: salvar a base tratada
# ===========================================================================
saida = PASTA_DADOS / "afazeres_tratado.csv"
sujo.to_csv(saida, index=False)   # index=False -> não salva a coluna de índice
print("Salvo em", saida)
# Excel: sujo.to_excel("arquivo.xlsx", index=False)

# ===========================================================================
# PARTE F — FORMATO LARGO x LONGO (melt) — muito útil para gráficos
# ===========================================================================
print("\n" + "=" * 70, "\nPARTE F — melt (largo -> longo)\n" + "=" * 70)
deso = pd.read_csv(PASTA_DADOS / "desocupacao_uf.csv")
print(deso.head(3))      # colunas taxa_2012 e taxa_2022 lado a lado (LARGO)
longo = deso.melt(id_vars=["uf", "regiao", "sexo"],
                  value_vars=["taxa_2012", "taxa_2022"],
                  var_name="ano", value_name="taxa")
longo["ano"] = longo["ano"].str.replace("taxa_", "").astype(int)
print(longo.head(3))     # agora 1 linha por UF/sexo/ano (LONGO) -> ótimo para px.bar(color="ano")

# Juntar duas tabelas: merge (como o PROCV do Excel)
pop = pd.DataFrame({"uf": ["BA", "SP"], "populacao_mi": [14.1, 44.4]})
print(deso.merge(pop, on="uf", how="inner").head())

print("\nFim da aula 02!")
