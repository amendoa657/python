"""
=============================================================================
AULA 05 — DASHBOARD STREAMLIT INTEGRADO ("painel unificado do grupo")
=============================================================================
Como rodar (na pasta do projeto):
    pip install -r requirements.txt
    streamlit run dashboard/app.py
  -> abre no navegador em http://localhost:8501

ATENÇÃO: NÃO rode com "python app.py". Streamlit roda com "streamlit run".

COMO O STREAMLIT FUNCIONA (entenda isso e você entende tudo):
  * O script inteiro roda de CIMA A BAIXO toda vez que o usuário mexe em
    QUALQUER widget (filtro, botão, upload). Não existe "evento" como em
    outras linguagens: cada clique = rodar o arquivo de novo.
  * Cada widget DEVOLVE o valor escolhido:
        ufs = st.multiselect("Estados", opcoes)   -> lista com o que foi marcado
        ano = st.slider("Ano", 2012, 2022)        -> número escolhido
  * Você usa esse valor para filtrar o DataFrame, e os gráficos/KPIs
    abaixo já usam o DataFrame filtrado. Pronto: filtros "funcionais".

COMANDOS MAIS USADOS (cola rápida):
  Texto ......... st.title  st.header  st.subheader  st.write  st.markdown  st.caption
  Avisos ........ st.info  st.success  st.warning  st.error
  Dados ......... st.dataframe(df)  st.table(df)  st.metric("rótulo", valor, delta)
  Gráficos ...... st.plotly_chart(fig)  st.pyplot(fig_matplotlib)  st.bar_chart(df)
  Mídia ......... st.image("arq.png" ou URL, caption=...)  st.video(url)
  Layout ........ st.columns(3)  st.tabs([...])  st.expander("...")  st.sidebar.xxx
  Entradas ...... st.file_uploader  st.selectbox  st.multiselect  st.slider
                  st.select_slider  st.radio  st.checkbox  st.button  st.text_input
  Controle ...... st.stop()  @st.cache_data  st.set_page_config(...)
=============================================================================
"""
import streamlit as st

# set_page_config TEM que ser o PRIMEIRO comando st do script (senão dá erro)
st.set_page_config(page_title="Números que Falam", page_icon="📊", layout="wide")

# Cada integrante do grupo faz o SEU módulo com uma função pagina().
# O app principal só importa e escolhe qual mostrar.
from modulos import afazeres, desocupacao  # noqa: E402

PAGINAS = {
    "🏠 Início": None,
    "🧹 Afazeres Domésticos": afazeres.pagina,
    "💼 Trabalho e Desocupação": desocupacao.pagina,
    # "🎓 Curso Superior": curso_superior.pagina,   <- outros integrantes
    # "📈 Crescimento Demográfico": demografia.pagina,
    # "🌎 IDH": idh.pagina,
}

# MENU DE NAVEGAÇÃO na barra lateral (requisito da Parte 2 do trabalho)
st.sidebar.title("📊 Números que Falam")
escolha = st.sidebar.radio("Indicador", list(PAGINAS.keys()))
st.sidebar.divider()

if PAGINAS[escolha] is None:
    st.title("📊 Números que Falam: Descobrindo o Brasil")
    st.markdown("""
Somos uma **startup de análise de dados** que transforma indicadores do IBGE em
decisões de política pública.

**Como usar:** escolha um indicador no menu à esquerda, envie sua base (CSV/XLSX)
ou use a base de exemplo, e ajuste os filtros.

Cada página traz:
1. **Filtros** na barra lateral
2. **KPIs** (cartões com os números principais)
3. **Estatística descritiva**: média, mediana, moda, quartis, IQR, amplitude, desvio padrão
4. **Outliers** pela regra 1,5 × IQR
5. **Gráficos** interativos (barras, boxplot, linha)
6. **Respostas** às perguntas das personas
7. **Notícias** de contexto
""")
else:
    PAGINAS[escolha]()   # chama a função pagina() do módulo escolhido
