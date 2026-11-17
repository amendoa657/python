"""
modulos/afazeres.py — PÁGINA INDIVIDUAL: Afazeres Domésticos (Persona 1)

Personas: Maria (BA), Fátima (PE), Antônio (AM), Luíza (CE).
Perguntas de negócio:
  1) Discrepância média de horas entre homens e mulheres por estado? E por gênero e raça?
  2) Como a divisão evoluiu nos estados analisados x média nacional?
  3) Há diferença entre quem trabalha fora (ocupado) e quem está desocupado?

Estrutura de TODA página de indicador (use como modelo na prova):
  1. Carregar dados (padrão ou upload)      -> critério 1 (ETL)
  2. Filtros na barra lateral               -> critério 1
  3. KPIs (st.metric)                       -> critério 2
  4. Tabela de estatísticas + outliers      -> critério 2
  5. Gráficos (barras, boxplot, linha)      -> critério 3
  6. Respostas às perguntas de negócio      -> critério 2 e 4
  7. Notícias e imagens                     -> critério 3
"""
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

from modulos.estatistica import carregar_padrao, ler_arquivo, resumo_estatistico, tabela_resumo

ARQUIVO_PADRAO = Path(__file__).parent.parent.parent / "dados" / "afazeres_domesticos.csv"
COLUNAS_OBRIGATORIAS = {"uf", "ano", "sexo", "raca", "faixa_etaria", "condicao", "horas_semanais"}


def pagina():
    st.title("🏠 Afazeres Domésticos e Cuidado")
    st.caption("Horas semanais dedicadas a afazeres domésticos e cuidado de pessoas — "
               "dados FICTÍCIOS no formato da Tabela 1.1 do IBGE (para estudo).")

    # -----------------------------------------------------------------------
    # 1. CARREGAR DADOS — upload OU arquivo padrão
    # -----------------------------------------------------------------------
    st.sidebar.subheader("📂 Dados")
    arquivo = st.sidebar.file_uploader("Envie a base (CSV ou XLSX)", type=["csv", "xlsx"],
                                       key="up_afazeres")   # key única evita conflito entre páginas
    if arquivo is not None:          # o usuário enviou algo
        try:
            df = ler_arquivo(arquivo)
            st.sidebar.success(f"Arquivo carregado: {arquivo.name}")
        except Exception as e:
            st.error(f"Erro ao ler o arquivo: {e}")
            st.stop()                # para a execução da página aqui
    else:
        df = carregar_padrao(str(ARQUIVO_PADRAO))

    # Validação: o arquivo tem as colunas que o código espera?
    faltando = COLUNAS_OBRIGATORIAS - set(df.columns)
    if faltando:
        st.error(f"O arquivo não tem as colunas: {sorted(faltando)}")
        st.stop()

    # ETL mínimo (caso o upload venha "sujo")
    df["uf"] = df["uf"].astype(str).str.strip().str.upper()
    df["horas_semanais"] = pd.to_numeric(df["horas_semanais"], errors="coerce")
    df = df.dropna(subset=["horas_semanais"]).drop_duplicates()

    # -----------------------------------------------------------------------
    # 2. FILTROS NA BARRA LATERAL
    # -----------------------------------------------------------------------
    st.sidebar.subheader("🔎 Filtros")
    todas_ufs = sorted(df["uf"].unique())
    padrao = [uf for uf in ["BA", "PE", "AM", "CE"] if uf in todas_ufs] or todas_ufs
    ufs = st.sidebar.multiselect("Estados", todas_ufs, default=padrao)

    anos = sorted(df["ano"].unique())
    ano_ini, ano_fim = st.sidebar.select_slider("Período", options=anos,
                                                value=(anos[0], anos[-1]))

    faixas = st.sidebar.multiselect("Faixa etária", sorted(df["faixa_etaria"].unique()),
                                    default=sorted(df["faixa_etaria"].unique()))
    racas = st.sidebar.multiselect("Cor/raça", sorted(df["raca"].unique()),
                                   default=sorted(df["raca"].unique()))
    condicoes = st.sidebar.multiselect("Condição de ocupação", sorted(df["condicao"].unique()),
                                       default=sorted(df["condicao"].unique()))

    # Aplica TODOS os filtros (cada condição entre parênteses, unidas com &)
    filtrado = df[
        (df["uf"].isin(ufs))
        & (df["ano"].between(ano_ini, ano_fim))
        & (df["faixa_etaria"].isin(faixas))
        & (df["raca"].isin(racas))
        & (df["condicao"].isin(condicoes))
    ]

    if filtrado.empty:               # proteção: filtro sem resultado quebraria os gráficos
        st.warning("Nenhum dado para os filtros escolhidos. Ajuste a barra lateral.")
        st.stop()

    # -----------------------------------------------------------------------
    # 3. KPIs
    # -----------------------------------------------------------------------
    mulheres = filtrado.loc[filtrado["sexo"] == "Mulheres", "horas_semanais"]
    homens = filtrado.loc[filtrado["sexo"] == "Homens", "horas_semanais"]
    diferenca = mulheres.mean() - homens.mean()

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Média — Mulheres", f"{mulheres.mean():.1f} h")
    c2.metric("Média — Homens", f"{homens.mean():.1f} h")
    c3.metric("Diferença (M − H)", f"{diferenca:.1f} h",
              help="Quantas horas a mais as mulheres dedicam por semana")
    c4.metric("Mediana geral", f"{filtrado['horas_semanais'].median():.1f} h")

    # -----------------------------------------------------------------------
    # 4. ESTATÍSTICAS DESCRITIVAS
    # -----------------------------------------------------------------------
    st.subheader("📐 Estatística descritiva")
    col_a, col_b = st.columns(2)
    r_m = resumo_estatistico(mulheres)
    r_h = resumo_estatistico(homens)
    with col_a:
        st.markdown("**Mulheres**")
        st.dataframe(tabela_resumo(r_m), hide_index=True)
    with col_b:
        st.markdown("**Homens**")
        st.dataframe(tabela_resumo(r_h), hide_index=True)

    # Outliers: mostra QUAIS registros são (por sexo, pois as distribuições são diferentes)
    def eh_outlier(x):
        q1, q3 = x.quantile(0.25), x.quantile(0.75)
        iqr = q3 - q1
        return (x < q1 - 1.5 * iqr) | (x > q3 + 1.5 * iqr)

    marcados = filtrado.assign(
        outlier=filtrado.groupby("sexo")["horas_semanais"].transform(eh_outlier))
    out = marcados[marcados["outlier"]]
    with st.expander(f"⚠️ Outliers encontrados (regra 1,5×IQR): {len(out)}"):
        if out.empty:
            st.write("Nenhum outlier nos filtros atuais.")
        else:
            st.dataframe(out.drop(columns="outlier"), hide_index=True)
            sem = marcados[~marcados["outlier"]]
            st.write(f"Média geral **com** outliers: {filtrado['horas_semanais'].mean():.2f} h — "
                     f"**sem** outliers: {sem['horas_semanais'].mean():.2f} h. "
                     f"Mediana com: {filtrado['horas_semanais'].median():.2f} h — "
                     f"sem: {sem['horas_semanais'].median():.2f} h. "
                     "A mediana quase não muda: por isso ela é a medida mais robusta.")

    # -----------------------------------------------------------------------
    # 5. GRÁFICOS
    # -----------------------------------------------------------------------
    st.subheader("📊 Visualizações")
    aba1, aba2, aba3 = st.tabs(["Barras por estado", "Boxplot", "Evolução x Brasil"])

    with aba1:
        media_uf = filtrado.groupby(["uf", "sexo"], as_index=False)["horas_semanais"].mean()
        fig = px.bar(media_uf, x="uf", y="horas_semanais", color="sexo", barmode="group",
                     text_auto=".1f",
                     labels={"uf": "Estado", "horas_semanais": "Horas semanais (média)",
                             "sexo": "Sexo"},
                     title="Horas semanais por estado e sexo")
        st.plotly_chart(fig)

    with aba2:
        fig = px.box(filtrado, x="sexo", y="horas_semanais", color="raca", points="outliers",
                     labels={"sexo": "Sexo", "horas_semanais": "Horas semanais", "raca": "Cor/raça"},
                     title="Distribuição das horas (caixa = Q1 a Q3, linha = mediana)")
        st.plotly_chart(fig)

    with aba3:
        # média dos estados filtrados x média NACIONAL (base inteira, mesmo período)
        sel = filtrado.groupby(["ano", "sexo"], as_index=False)["horas_semanais"].mean()
        sel["recorte"] = "Estados selecionados"
        nac = (df[df["ano"].between(ano_ini, ano_fim)]
               .groupby(["ano", "sexo"], as_index=False)["horas_semanais"].mean())
        nac["recorte"] = "Média nacional"
        evol = pd.concat([sel, nac])
        fig = px.line(evol, x="ano", y="horas_semanais", color="sexo", line_dash="recorte",
                      markers=True,
                      labels={"ano": "Ano", "horas_semanais": "Horas semanais (média)"},
                      title="Evolução: estados selecionados x média nacional")
        st.plotly_chart(fig)

    # -----------------------------------------------------------------------
    # 6. RESPOSTAS ÀS PERGUNTAS DE NEGÓCIO (texto gerado a partir dos números)
    # -----------------------------------------------------------------------
    st.subheader("💼 Respostas para as gestoras e gestores")

    # P1 — por estado
    pivo = filtrado.pivot_table(index="uf", columns="sexo", values="horas_semanais", aggfunc="mean")
    pivo["Diferença (h)"] = pivo["Mulheres"] - pivo["Homens"]
    st.markdown("**1) Discrepância média entre mulheres e homens, por estado**")
    st.dataframe(pivo.round(1).sort_values("Diferença (h)", ascending=False))

    # P1b — gênero x raça
    grupo = (filtrado.groupby(["sexo", "raca"])["horas_semanais"]
             .agg(["mean", "median"]).round(1)
             .rename(columns={"mean": "Média (h)", "median": "Mediana (h)"}))
    st.markdown("**Por gênero e raça**")
    st.dataframe(grupo)

    # P3 — ocupadas x desocupadas
    cond = filtrado.groupby(["sexo", "condicao"])["horas_semanais"].median().unstack()
    st.markdown("**3) Ocupados x desocupados (mediana de horas)**")
    st.dataframe(cond.round(1))

    maior = pivo["Diferença (h)"].idxmax()
    st.info(
        f"📌 Nos estados selecionados, as mulheres dedicam em média **{diferenca:.1f} h a mais** "
        f"por semana que os homens. A maior diferença está em **{maior}** "
        f"({pivo.loc[maior, 'Diferença (h)']:.1f} h). O desvio padrão das mulheres "
        f"({r_m['desvio_padrao']:.1f} h) indica o quanto os estados variam entre si. "
        "Recomendação: priorizar políticas de economia do cuidado (creches, "
        "licença parental compartilhada) nos estados com maior diferença."
    )

    # -----------------------------------------------------------------------
    # 7. NOTÍCIAS E IMAGENS (conteúdo de mídia)
    # -----------------------------------------------------------------------
    st.subheader("📰 Contexto: carga mental feminina e economia do cuidado")
    n1, n2 = st.columns(2)
    with n1:
        # st.image("imagens/cuidado.jpg", caption="...")  # <- imagem local (mais seguro que URL)
        st.markdown("### 🧠 Carga mental feminina")
        st.write("Além das horas de trabalho doméstico, as mulheres acumulam o "
                 "planejamento invisível da casa e do cuidado com a família.")
        st.markdown("[Agência de Notícias do IBGE](https://agenciadenoticias.ibge.gov.br/)")
    with n2:
        st.markdown("### 💰 Economia do cuidado")
        st.write("O trabalho de cuidado não remunerado sustenta a economia, mas "
                 "não aparece no PIB. Medir essas horas é o primeiro passo para políticas públicas.")
        st.markdown("[IBGE — Estatísticas de Gênero](https://www.ibge.gov.br/)")

    # Download da base filtrada (bônus de ETL "Load")
    st.download_button("⬇️ Baixar dados filtrados (CSV)",
                       filtrado.to_csv(index=False).encode("utf-8"),
                       file_name="afazeres_filtrado.csv", mime="text/csv")
