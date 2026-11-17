"""
modulos/desocupacao.py — PÁGINA INDIVIDUAL: Trabalho e Desocupação (Persona 6)

Personas: Márcia (Ministra do Trabalho), Renato (Indústria), Sílvia (Sebrae).
Perguntas:
  1) Taxa de desocupação por UF comparando 2012 e 2022?
  2) Idem, por gênero?
  3) Qual estado mais reduziu o desemprego?

Mostra um segundo "integrante" do grupo usando o MESMO módulo de estatística.
"""
from pathlib import Path

import plotly.express as px
import streamlit as st

from modulos.estatistica import carregar_padrao, ler_arquivo, resumo_estatistico, tabela_resumo

ARQUIVO_PADRAO = Path(__file__).parent.parent.parent / "dados" / "desocupacao_uf.csv"


def pagina():
    st.title("💼 Trabalho e Desocupação")
    st.caption("Taxa de desocupação (%) por UF e sexo, 2012 x 2022 — dados FICTÍCIOS para estudo.")

    arquivo = st.sidebar.file_uploader("Envie a base (CSV ou XLSX)", type=["csv", "xlsx"],
                                       key="up_deso")
    df = ler_arquivo(arquivo) if arquivo else carregar_padrao(str(ARQUIVO_PADRAO))

    # Filtros
    regioes = st.sidebar.multiselect("Região", sorted(df["regiao"].unique()),
                                     default=sorted(df["regiao"].unique()))
    sexo = st.sidebar.radio("Sexo", ["Ambos", "Homens", "Mulheres"], horizontal=True)

    f = df[df["regiao"].isin(regioes)]
    if sexo != "Ambos":
        f = f[f["sexo"] == sexo]
    if f.empty:
        st.warning("Nenhum dado para esses filtros.")
        st.stop()

    # Média por UF (se "Ambos", junta homens e mulheres)
    por_uf = f.groupby("uf", as_index=False)[["taxa_2012", "taxa_2022"]].mean()
    por_uf["variacao_pp"] = por_uf["taxa_2022"] - por_uf["taxa_2012"]   # pontos percentuais

    c1, c2, c3 = st.columns(3)
    c1.metric("Mediana 2012", f"{por_uf['taxa_2012'].median():.1f}%")
    c2.metric("Mediana 2022", f"{por_uf['taxa_2022'].median():.1f}%",
              delta=f"{por_uf['taxa_2022'].median() - por_uf['taxa_2012'].median():.1f} p.p.",
              delta_color="inverse")   # inverse: subir desemprego aparece em vermelho
    melhor = por_uf.loc[por_uf["variacao_pp"].idxmin()]
    c3.metric("Maior redução", melhor["uf"], f"{melhor['variacao_pp']:.1f} p.p.",
              delta_color="inverse")

    st.subheader("📐 Estatísticas de 2022 entre as UFs")
    st.dataframe(tabela_resumo(resumo_estatistico(por_uf["taxa_2022"])), hide_index=True)

    longo = por_uf.melt(id_vars="uf", value_vars=["taxa_2012", "taxa_2022"],
                        var_name="ano", value_name="taxa")
    longo["ano"] = longo["ano"].str.replace("taxa_", "")
    fig = px.bar(longo.sort_values("taxa"), x="uf", y="taxa", color="ano", barmode="group",
                 labels={"uf": "UF", "taxa": "Taxa de desocupação (%)", "ano": "Ano"},
                 title="Desocupação por UF: 2012 x 2022")
    st.plotly_chart(fig)

    fig = px.box(f.melt(id_vars=["uf", "sexo"], value_vars=["taxa_2012", "taxa_2022"],
                        var_name="ano", value_name="taxa"),
                 x="ano", y="taxa", color="sexo", points="all", hover_name="uf",
                 labels={"taxa": "Taxa (%)", "ano": ""}, title="Dispersão entre as UFs")
    st.plotly_chart(fig)

    st.info(f"📌 O estado que mais reduziu a desocupação foi **{melhor['uf']}** "
            f"({melhor['variacao_pp']:.1f} pontos percentuais).")
