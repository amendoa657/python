"""
GABARITO 06 — App Streamlit (9 erros)

 #  Erro original                                     Sintoma                                        Correção
 1  st.title ANTES de st.set_page_config               Em versões ANTIGAS do Streamlit (as de escola,  set_page_config deve ser o 1º comando st
                                                       geralmente): StreamlitAPIException "set_page_   (nas versões novas não quebra, mas continua
                                                       config() can only be called once... first       sendo a boa prática e o professor cobra)
                                                       Streamlit command"
 2  pd.read_csv(arquivo) sem checar None               ValueError ao abrir o app (nada enviado ainda)   if arquivo is not None: ... else: base padrão
 3  st.multiselect (fora da sidebar)                   filtro aparece no meio da página (requisito)     st.sidebar.multiselect
 4  default=["Bahia"]                                  StreamlitAPIException: default não está          default precisa existir nas opções: ["BA"]
                                                       nas opções
 5  (df["ano"] <= anos[0])                              roda, mas só mostra 1 ano (lógica)              anos[1] -> o slider de intervalo devolve (inicio, fim)
 6  aviso de vazio sem st.stop()                        segue executando e quebra/mostra NaN            st.stop() logo depois do warning
 7  c1.metric("Média", h.mean)                          mostra "<bound method...>" ou erro              h.mean() e formatar: f"{h.mean():.1f} h"
 8  groupby em df (e não em filtrado)                   gráfico NÃO muda com os filtros (lógica!)       usar filtrado -> "filtros funcionais" da rubrica
 9  st.pyplot(fig) com figura Plotly                    erro/figura não aparece                         st.plotly_chart(fig)  (st.pyplot é para matplotlib)
"""
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Afazeres", layout="wide")          # CORRIGIDO (1): primeiro!
st.title("Afazeres Domésticos")

arquivo = st.sidebar.file_uploader("Envie o CSV", type=["csv"])
if arquivo is not None:                                            # CORRIGIDO (2)
    df = pd.read_csv(arquivo)
else:
    df = pd.read_csv(Path(__file__).resolve().parents[2] / "dados" / "afazeres_domesticos.csv")

opcoes = sorted(df["uf"].unique())
ufs = st.sidebar.multiselect("Estados", opcoes,                    # CORRIGIDO (3)
                             default=[u for u in ["BA"] if u in opcoes])   # CORRIGIDO (4)
anos = st.sidebar.slider("Anos", int(df["ano"].min()), int(df["ano"].max()),
                         (int(df["ano"].min()), int(df["ano"].max())))

filtrado = df[df["uf"].isin(ufs) & (df["ano"] >= anos[0]) & (df["ano"] <= anos[1])]  # CORRIGIDO (5)

if filtrado.empty:
    st.warning("Nenhum dado para esse filtro.")
    st.stop()                                                      # CORRIGIDO (6)

h = filtrado["horas_semanais"]
q1, q3 = h.quantile(0.25), h.quantile(0.75)
iqr = q3 - q1
n_out = int(((h < q1 - 1.5 * iqr) | (h > q3 + 1.5 * iqr)).sum())

c1, c2, c3 = st.columns(3)
c1.metric("Média", f"{h.mean():.1f} h")                            # CORRIGIDO (7)
c2.metric("Mediana", f"{h.median():.1f} h")
c3.metric("Outliers", n_out)

media_uf = filtrado.groupby(["uf", "sexo"], as_index=False)["horas_semanais"].mean()  # CORRIGIDO (8)
fig = px.bar(media_uf, x="uf", y="horas_semanais", color="sexo", barmode="group",
             labels={"uf": "Estado", "horas_semanais": "Horas semanais"})
st.plotly_chart(fig)                                               # CORRIGIDO (9)

fig2 = px.box(filtrado, x="sexo", y="horas_semanais", points="outliers",
              labels={"horas_semanais": "Horas semanais", "sexo": "Sexo"})
st.plotly_chart(fig2)
