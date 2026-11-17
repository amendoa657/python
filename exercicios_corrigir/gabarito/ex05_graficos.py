"""
GABARITO 05 — Gráficos (6 erros)

 #  Erro original                  Sintoma                               Correção
 1  x="UF"                         ValueError: "UF" não é coluna        x="uf" (nome exato da coluna, minúsculo)
 2  barmode="grouped"              ValueError (valor inválido)          barmode="group"  (ou "stack", "relative", "overlay")
 3  label={...}                    TypeError: unexpected keyword        labels={...}  (com S)
 4  px.boxplot                     AttributeError                       px.box
 5  linha com df sem agrupar       roda, mas desenha um "rabisco"        agrupar antes: groupby(["ano","sexo"]).mean()
 6  pasta graficos_gerados pode    FileNotFoundError ao salvar           criar a pasta: os.makedirs(..., exist_ok=True)
    não existir
"""
import os
import pandas as pd
import plotly.express as px

os.makedirs("graficos_gerados", exist_ok=True)                    # CORRIGIDO (6)
df = pd.read_csv("dados/afazeres_domesticos.csv")

# 1) Barras
sel = df[df["uf"].isin(["BA", "PE", "AM", "CE"])]
media = sel.groupby(["uf", "sexo"], as_index=False)["horas_semanais"].mean()
fig1 = px.bar(media, x="uf", y="horas_semanais", color="sexo",   # CORRIGIDO (1)
              barmode="group",                                     # CORRIGIDO (2)
              labels={"horas_semanais": "Horas por semana", "uf": "Estado"},  # CORRIGIDO (3)
              title="Horas por estado e sexo")
fig1.write_html("graficos_gerados/ex05_barras.html")

# 2) Boxplot
fig2 = px.box(df, x="sexo", y="horas_semanais", points="outliers",   # CORRIGIDO (4)
              title="Distribuição das horas")
fig2.write_html("graficos_gerados/ex05_box.html")

# 3) Linha
evol = df.groupby(["ano", "sexo"], as_index=False)["horas_semanais"].mean()  # CORRIGIDO (5)
fig3 = px.line(evol, x="ano", y="horas_semanais", color="sexo", markers=True,
               title="Evolução da média de horas")
fig3.write_html("graficos_gerados/ex05_linha.html")
print("Gráficos gerados!")
