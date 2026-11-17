"""
EXERCÍCIO 06 — App Streamlit completo        (9 erros)
-----------------------------------------------------------------
Este é o tipo de código mais provável de cair: um mini-dashboard.

Requisitos do app (o que DEVERIA acontecer):
  - Título e configuração da página
  - Upload de CSV na barra lateral; se nada for enviado, usar a base padrão
  - Filtros NA BARRA LATERAL: estados (multiselect) e intervalo de anos (slider)
  - KPIs: média e mediana de horas, e nº de outliers (regra 1,5×IQR)
  - Gráfico de barras e boxplot que MUDAM quando mexo nos filtros
  - Mensagem de aviso se o filtro não retornar dados

Rode:  streamlit run exercicios_corrigir/ex06_streamlit_app.py
(a partir da pasta do projeto)
DICA: alguns erros só aparecem quando você INTERAGE (mexe no filtro,
envia arquivo) ou quando OLHA o resultado (gráfico não muda).
Gabarito: exercicios_corrigir/gabarito/ex06_streamlit_app.py
"""
import pandas as pd
import plotly.express as px
import streamlit as st

st.title("Afazeres Domésticos")
st.set_page_config(page_title="Afazeres", layout="wide")

arquivo = st.sidebar.file_uploader("Envie o CSV", type=["csv"])
df = pd.read_csv(arquivo)

ufs = st.multiselect("Estados", sorted(df["uf"].unique()), default=["Bahia"])
anos = st.sidebar.slider("Anos", int(df["ano"].min()), int(df["ano"].max()),
                         (int(df["ano"].min()), int(df["ano"].max())))

filtrado = df[df["uf"].isin(ufs) & (df["ano"] >= anos[0]) & (df["ano"] <= anos[0])]

if filtrado.empty:
    st.warning("Nenhum dado para esse filtro.")

h = filtrado["horas_semanais"]
q1, q3 = h.quantile(0.25), h.quantile(0.75)
iqr = q3 - q1
n_out = ((h < q1 - 1.5 * iqr) | (h > q3 + 1.5 * iqr)).sum()

c1, c2, c3 = st.columns(3)
c1.metric("Média", h.mean)
c2.metric("Mediana", f"{h.median():.1f} h")
c3.metric("Outliers", n_out)

media_uf = df.groupby(["uf", "sexo"], as_index=False)["horas_semanais"].mean()
fig = px.bar(media_uf, x="uf", y="horas_semanais", color="sexo", barmode="group")
st.pyplot(fig)

fig2 = px.box(filtrado, x="sexo", y="horas_semanais")
st.plotly_chart(fig2)
