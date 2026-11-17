"""
modulos/estatistica.py — funções de estatística e carregamento reaproveitadas
por TODAS as páginas do dashboard (cada integrante do grupo importa daqui).

Separar funções em um módulo = "não repetir código" (boa prática cobrada).
"""
import pandas as pd
import streamlit as st


def resumo_estatistico(serie: pd.Series) -> dict:
    """Calcula todas as medidas exigidas pela rubrica para uma coluna numérica."""
    serie = pd.to_numeric(serie, errors="coerce").dropna()   # garante número e tira NaN
    if serie.empty:
        return {}
    q1 = serie.quantile(0.25)
    q3 = serie.quantile(0.75)
    iqr = q3 - q1
    lim_inf = q1 - 1.5 * iqr
    lim_sup = q3 + 1.5 * iqr
    moda = serie.mode()
    return {
        "n": int(serie.count()),
        "media": serie.mean(),
        "mediana": serie.median(),
        "moda": moda.iloc[0] if not moda.empty else None,
        "minimo": serie.min(),
        "maximo": serie.max(),
        "amplitude": serie.max() - serie.min(),
        "variancia": serie.var(),          # amostral (ddof=1)
        "desvio_padrao": serie.std(),      # amostral (ddof=1) = raiz da variância
        "q1": q1,
        "q3": q3,
        "iqr": iqr,
        "lim_inf": lim_inf,
        "lim_sup": lim_sup,
        "outliers": serie[(serie < lim_inf) | (serie > lim_sup)],
    }


def tabela_resumo(r: dict) -> pd.DataFrame:
    """Transforma o dicionário do resumo em uma tabela bonita para st.dataframe."""
    nomes = {
        "n": "Quantidade (n)", "media": "Média", "mediana": "Mediana", "moda": "Moda",
        "minimo": "Mínimo", "maximo": "Máximo", "amplitude": "Amplitude",
        "variancia": "Variância", "desvio_padrao": "Desvio padrão",
        "q1": "Q1 (25%)", "q3": "Q3 (75%)", "iqr": "IQR (Q3 − Q1)",
        "lim_inf": "Limite inferior (Q1 − 1,5·IQR)", "lim_sup": "Limite superior (Q3 + 1,5·IQR)",
    }
    linhas = [(nomes[k], round(float(v), 2)) for k, v in r.items() if k in nomes and v is not None]
    linhas.append(("Nº de outliers", len(r["outliers"])))
    return pd.DataFrame(linhas, columns=["Medida", "Valor"])


def ler_arquivo(arquivo) -> pd.DataFrame:
    """Lê CSV ou XLSX vindo do st.file_uploader OU de um caminho no disco.

    Tenta os formatos mais comuns do IBGE (vírgula/ponto-e-vírgula, utf-8/latin-1).
    """
    nome = getattr(arquivo, "name", str(arquivo)).lower()
    if nome.endswith((".xlsx", ".xls")):
        return pd.read_excel(arquivo)           # precisa do pacote openpyxl
    # CSV: tenta combinações até uma funcionar
    for sep, dec, enc in [(",", ".", "utf-8"), (";", ",", "utf-8"), (";", ",", "latin-1")]:
        try:
            if hasattr(arquivo, "seek"):
                arquivo.seek(0)                 # volta ao início do arquivo enviado
            df = pd.read_csv(arquivo, sep=sep, decimal=dec, encoding=enc,
                             na_values=["...", "-", "X", ""])
            if df.shape[1] > 1:                 # se leu só 1 coluna, o separador estava errado
                return df
        except (UnicodeDecodeError, pd.errors.ParserError):
            continue
    raise ValueError("Não consegui ler o arquivo. Verifique o separador e a codificação.")


@st.cache_data   # guarda o resultado em cache: não relê o arquivo a cada clique
def carregar_padrao(caminho: str) -> pd.DataFrame:
    return pd.read_csv(caminho)
