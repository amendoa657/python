"""
EXERCÍCIO 05 — Gráficos com Plotly        (6 erros)
-----------------------------------------------------------------
Objetivo: gerar 3 gráficos da base de afazeres domésticos:
  1) barras agrupadas: média de horas por estado (BA, PE, AM, CE) e sexo
  2) boxplot: distribuição das horas por sexo, mostrando outliers
  3) linha: evolução da média de horas por ano e sexo (1 ponto por ano!)
Os arquivos .html vão para a pasta graficos_gerados/.

Rode a partir da pasta do projeto:  python exercicios_corrigir/ex05_graficos.py
Gabarito: exercicios_corrigir/gabarito/ex05_graficos.py
"""
import pandas as pd
import plotly.express as px

df = pd.read_csv("dados/afazeres_domesticos.csv")

# 1) Barras
sel = df[df["uf"].isin(["BA", "PE", "AM", "CE"])]
media = sel.groupby(["uf", "sexo"], as_index=False)["horas_semanais"].mean()
fig1 = px.bar(media, x="UF", y="horas_semanais", color="sexo", barmode="grouped",
              label={"horas_semanais": "Horas por semana"},
              title="Horas por estado e sexo")
fig1.write_html("graficos_gerados/ex05_barras.html")

# 2) Boxplot
fig2 = px.boxplot(df, x="sexo", y="horas_semanais", points="outliers",
                  title="Distribuição das horas")
fig2.write_html("graficos_gerados/ex05_box.html")

# 3) Linha
fig3 = px.line(df, x="ano", y="horas_semanais", color="sexo", markers=True,
               title="Evolução da média de horas")
fig3.write_html("graficos_gerados/ex05_linha.html")
print("Gráficos gerados!")
