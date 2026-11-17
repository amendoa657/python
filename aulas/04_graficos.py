"""
=============================================================================
AULA 04 — GRÁFICOS COM PLOTLY EXPRESS (e quando usar cada um)
=============================================================================
Como rodar:  python aulas/04_graficos.py
  -> gera arquivos .html na pasta graficos_gerados/ (abra no navegador)

Plotly Express (px) faz gráficos INTERATIVOS (passa o mouse e vê o valor).
No Streamlit, você mostra qualquer um deles com:  st.plotly_chart(fig)

RECEITA de quase todo gráfico px:
    fig = px.TIPO(dataframe, x="coluna", y="coluna", color="coluna", title="...")
    fig.show()            # no Python/Jupyter
    st.plotly_chart(fig)  # no Streamlit

QUAL GRÁFICO USAR? (escolha errada derruba nota no critério 3)
  | Pergunta                                   | Gráfico              | px              |
  |--------------------------------------------|----------------------|-----------------|
  | Comparar categorias (UF, sexo)             | Barras               | px.bar          |
  | Ver dispersão, quartis e OUTLIERS          | Boxplot              | px.box          |
  | Evolução no TEMPO (anos)                   | Linha                | px.line         |
  | Distribuição / assimetria de 1 variável    | Histograma           | px.histogram    |
  | Partes de um todo (% de cada modal)        | Pizza / Rosca        | px.pie (hole=)  |
  | Relação entre 2 variáveis numéricas        | Dispersão (scatter)  | px.scatter      |
  | Proporção dentro de cada grupo (100%)      | Barras empilhadas %  | px.bar + barnorm|
  | Pirâmide etária                            | Barras horizontais   | go.Bar          |
  | Comparar várias dimensões (IDH)            | Radar                | px.line_polar   |
=============================================================================
"""
from pathlib import Path
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

RAIZ = Path(__file__).parent.parent
SAIDA = RAIZ / "graficos_gerados"
SAIDA.mkdir(exist_ok=True)

df = pd.read_csv(RAIZ / "dados" / "afazeres_domesticos.csv")
deso = pd.read_csv(RAIZ / "dados" / "desocupacao_uf.csv")

def salvar(fig, nome):
    fig.write_html(SAIDA / f"{nome}.html")
    print("gerado:", nome)

# ---------------------------------------------------------------------------
# 1. BARRAS AGRUPADAS — horas por estado e sexo
# ---------------------------------------------------------------------------
# Para gráfico de barras, normalmente AGRUPAMOS antes (1 valor por barra).
media = (df[df["uf"].isin(["BA", "PE", "AM", "CE"])]
         .groupby(["uf", "sexo"], as_index=False)["horas_semanais"].mean())
fig = px.bar(media, x="uf", y="horas_semanais", color="sexo",
             barmode="group",               # "group" = lado a lado | "stack" = empilhado
             text_auto=".1f",               # mostra o valor em cima da barra
             labels={"uf": "Estado", "horas_semanais": "Horas por semana", "sexo": "Sexo"},
             title="Média de horas semanais em afazeres domésticos por estado e sexo")
salvar(fig, "1_barras")
# Rótulo de eixo é COBRADO na rubrica -> use labels={...} sempre.

# ---------------------------------------------------------------------------
# 2. BOXPLOT — dispersão e outliers
# ---------------------------------------------------------------------------
# COMO LER UM BOXPLOT:
#   - linha no meio da caixa = MEDIANA (Q2)
#   - base da caixa = Q1 ; topo da caixa = Q3  -> altura da caixa = IQR
#   - "bigodes" vão até o último valor DENTRO de Q1-1,5×IQR e Q3+1,5×IQR
#   - pontinhos soltos fora dos bigodes = OUTLIERS
#   - caixa alta = muita dispersão ; caixa baixa = dados homogêneos
#   - mediana fora do centro da caixa = assimetria
fig = px.box(df, x="sexo", y="horas_semanais", color="raca",
             points="outliers",             # mostra só os outliers como pontos ("all" mostra todos)
             labels={"horas_semanais": "Horas por semana", "sexo": "Sexo", "raca": "Cor/raça"},
             title="Distribuição de horas por sexo e raça (boxplot)")
salvar(fig, "2_boxplot")

# ---------------------------------------------------------------------------
# 3. LINHA — evolução temporal
# ---------------------------------------------------------------------------
evol = df.groupby(["ano", "sexo"], as_index=False)["horas_semanais"].mean()
fig = px.line(evol, x="ano", y="horas_semanais", color="sexo", markers=True,
              labels={"ano": "Ano", "horas_semanais": "Horas por semana"},
              title="Evolução da média nacional de horas")
salvar(fig, "3_linha")
# ERRO COMUM: fazer linha com dados NÃO agrupados -> vira um "rabisco" (vários pontos por ano)
# ERRO COMUM: x sem ordenar -> a linha vai e volta. Use df.sort_values("ano") antes.

# ---------------------------------------------------------------------------
# 4. HISTOGRAMA — forma da distribuição + linhas de média e mediana
# ---------------------------------------------------------------------------
fig = px.histogram(df, x="horas_semanais", nbins=30, color="sexo", opacity=0.7,
                   labels={"horas_semanais": "Horas por semana"},
                   title="Histograma de horas (média x mediana)")
fig.add_vline(x=df["horas_semanais"].mean(), line_dash="dash", line_color="red",
              annotation_text="Média")
fig.add_vline(x=df["horas_semanais"].median(), line_dash="dot", line_color="black",
              annotation_text="Mediana")
salvar(fig, "4_histograma")
# Se a média fica à DIREITA da mediana -> assimetria positiva (cauda à direita).

# ---------------------------------------------------------------------------
# 5. PIZZA / ROSCA — composição (partes de um todo)
# ---------------------------------------------------------------------------
modais = pd.DataFrame({"modal": ["Ônibus/metrô", "Carro/moto", "A pé/bicicleta"],
                       "pessoas": [45, 35, 20]})
fig = px.pie(modais, names="modal", values="pessoas", hole=0.4,   # hole -> rosca
             title="Modal de transporte predominante (exemplo)")
salvar(fig, "5_rosca")
# Use pizza com POUCAS categorias (até ~6). Muitas fatias = gráfico poluído.

# ---------------------------------------------------------------------------
# 6. DISPERSÃO (scatter) — relação entre 2 números
# ---------------------------------------------------------------------------
fig = px.scatter(deso, x="taxa_2012", y="taxa_2022", color="regiao", hover_name="uf",
                 symbol="sexo",
                 labels={"taxa_2012": "Desocupação 2012 (%)", "taxa_2022": "Desocupação 2022 (%)"},
                 title="Desocupação 2012 x 2022 por UF")
salvar(fig, "6_dispersao")
print("correlação 2012 x 2022:", round(deso["taxa_2012"].corr(deso["taxa_2022"]), 2))
# Correlação vai de -1 a 1. Perto de 1 = sobem juntos. Perto de 0 = sem relação.
# CORRELAÇÃO NÃO É CAUSALIDADE!

# ---------------------------------------------------------------------------
# 7. BARRAS 100% EMPILHADAS — proporção (ex.: % de mulheres por área)
# ---------------------------------------------------------------------------
cursos = pd.DataFrame({
    "area": ["Exatas", "Exatas", "Humanas", "Humanas", "Saúde", "Saúde"],
    "sexo": ["Mulheres", "Homens"] * 3,
    "diplomados": [3000, 7000, 6500, 3500, 7200, 2800]})
# Jeito 1 (didático): calcular o % na mão com groupby + transform
cursos["pct"] = cursos["diplomados"] / cursos.groupby("area")["diplomados"].transform("sum") * 100
fig = px.bar(cursos, x="area", y="pct", color="sexo", text_auto=".0f",
             labels={"pct": "% dos diplomados", "area": "Área"},
             title="Proporção de gênero por área (barras 100%)")
# Jeito 2 (atalho): px.bar(cursos, x="area", y="diplomados", color="sexo")
#                   e depois fig.update_layout(barnorm="percent")
#   (barnorm é do LAYOUT, não do px.bar -> px.bar(..., barnorm=...) dá TypeError)
salvar(fig, "7_barras_100")

# ---------------------------------------------------------------------------
# 8. PIRÂMIDE ETÁRIA — barras horizontais, homens com valor NEGATIVO
# ---------------------------------------------------------------------------
faixas = ["0-14", "15-29", "30-44", "45-59", "60+"]
homens = [20, 24, 22, 17, 13]
mulheres = [19, 23, 22, 18, 16]
fig = go.Figure()
fig.add_trace(go.Bar(y=faixas, x=[-h for h in homens], name="Homens", orientation="h"))
fig.add_trace(go.Bar(y=faixas, x=mulheres, name="Mulheres", orientation="h"))
fig.update_layout(barmode="relative", title="Pirâmide etária (exemplo, % da população)",
                  xaxis_title="% (homens à esquerda)", yaxis_title="Faixa etária")
salvar(fig, "8_piramide")

# ---------------------------------------------------------------------------
# 9. RADAR — comparar dimensões (IDH: longevidade, educação, renda)
# ---------------------------------------------------------------------------
idh = pd.DataFrame({"uf": ["MA"] * 3 + ["MG"] * 3,
                    "dimensao": ["Longevidade", "Educação", "Renda"] * 2,
                    "valor": [0.76, 0.56, 0.61, 0.84, 0.64, 0.73]})
fig = px.line_polar(idh, r="valor", theta="dimensao", color="uf", line_close=True,
                    title="Subíndices do IDHM (exemplo)")
salvar(fig, "9_radar")

# ---------------------------------------------------------------------------
# 10. MAPA COROPLÉTICO por UF (opcional) — precisa de um GeoJSON dos estados
# ---------------------------------------------------------------------------
# geo_url = "https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson"
# fig = px.choropleth(tabela, geojson=geo_url, locations="nome_estado",
#                     featureidkey="properties.name", color="valor")
# fig.update_geos(fitbounds="locations", visible=False)
# (Deixado comentado porque precisa de internet.)

# ---------------------------------------------------------------------------
# MATPLOTLIB (caso a prova use matplotlib em vez de plotly)
# ---------------------------------------------------------------------------
#   import matplotlib.pyplot as plt
#   fig, ax = plt.subplots()
#   ax.bar(media["uf"], media["horas_semanais"])
#   ax.set_xlabel("Estado"); ax.set_ylabel("Horas"); ax.set_title("Título")
#   ax.boxplot(df["horas_semanais"])
#   ax.hist(df["horas_semanais"], bins=20)
#   plt.show()          # no Python
#   st.pyplot(fig)      # no Streamlit  (NÃO é st.plotly_chart!)
print("\nAbra os arquivos .html da pasta graficos_gerados/ no navegador.")
