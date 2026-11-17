# ⚡ Resumo de 1 página (revisar 5 min antes da prova)

```python
import pandas as pd, numpy as np, plotly.express as px, streamlit as st

# LER
df = pd.read_csv("a.csv", sep=";", decimal=",", encoding="latin-1", skiprows=2, na_values=["...", "-"])
df = pd.read_excel("a.xlsx")
df.head(); df.shape; df.columns; df.dtypes; df.info(); df.describe()

# LIMPAR  (sempre atribuir: df = ...)
df = df.rename(columns={"Velho": "novo"})
df["uf"] = df["uf"].str.strip().str.upper()
df["x"] = pd.to_numeric(df["x"], errors="coerce")
df = df.dropna(subset=["x"]).drop_duplicates()

# FILTRAR   (& | ~  +  parênteses;  isin com LISTA)
f = df[(df["uf"].isin(["BA", "PE"])) & (df["ano"].between(2016, 2022))]

# AGRUPAR
df.groupby(["uf", "sexo"], as_index=False)["x"].mean()
df.groupby("sexo")["x"].agg(["mean", "median", "std"])
df.pivot_table(index="uf", columns="sexo", values="x", aggfunc="mean")

# ESTATÍSTICA
s = df["x"]
s.mean(); s.median(); s.mode()[0]; s.max() - s.min()
s.var(); s.std()                     # amostral (n-1). np.std(s) = populacional (n)
q1, q3 = s.quantile(0.25), s.quantile(0.75); iqr = q3 - q1
li, ls = q1 - 1.5*iqr, q3 + 1.5*iqr
outliers = s[(s < li) | (s > ls)]

# GRÁFICOS
px.bar(d, x="uf", y="x", color="sexo", barmode="group", labels={"x": "Horas"}, title="...")
px.box(df, x="sexo", y="x", points="outliers")
px.line(d.sort_values("ano"), x="ano", y="x", color="sexo", markers=True)
px.histogram(df, x="x", nbins=30);  px.pie(d, names="cat", values="v", hole=.4)

# STREAMLIT  (rodar: streamlit run app.py)
st.set_page_config(page_title="...", layout="wide")         # 1º comando
arq = st.sidebar.file_uploader("CSV/XLSX", type=["csv", "xlsx"])
if arq is not None:
    df = pd.read_excel(arq) if arq.name.endswith(".xlsx") else pd.read_csv(arq)
ufs = st.sidebar.multiselect("UF", opcoes, default=opcoes)
a0, a1 = st.sidebar.slider("Ano", 2012, 2022, (2012, 2022))
f = df[(df["uf"].isin(ufs)) & (df["ano"].between(a0, a1))]
if f.empty: st.warning("Sem dados"); st.stop()
c1, c2 = st.columns(2); c1.metric("Média", f"{f['x'].mean():.1f}")
st.plotly_chart(fig);  st.dataframe(f);  st.image("img.png");  st.markdown("[link](https://...)")
```

| Conceito | Fórmula | Lembrete |
|---|---|---|
| Média | Σx / n | sensível a outlier |
| Mediana | valor do meio (ordenado) | robusta; n par = média dos 2 do meio |
| Moda | mais frequente | categóricos |
| Amplitude | máx − mín | |
| Variância | Σ(x−média)² / n (ou n−1) | unidade² |
| Desvio padrão | √variância | mesma unidade; alto = heterogêneo |
| IQR | Q3 − Q1 | 50% centrais |
| Outlier | < Q1−1,5·IQR **ou** > Q3+1,5·IQR | |
| média > mediana | assimetria à **direita** | renda |

**Fala de consultor:** número → significado → decisão.
