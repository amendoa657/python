# 📊 Números que Falam: Projeto de Estudo Completo

Material para estudar **Python + Pandas + Estatística + Streamlit** no formato do
Projeto Integrador "Números que Falam: Descobrindo o Brasil" (dashboard de indicadores do IBGE).

> ⚠️ Os dados em `dados/` são **fictícios**, mas imitam o formato real do IBGE. Servem só para treinar.

---

## 🗺️ Ordem de estudo (se você tem pouco tempo)

| Ordem | Arquivo | O que aprende | Tempo |
|---|---|---|---|
| 1 | [`COLA.md`](COLA.md) | resumo de tudo em 1 página | 5 min |
| 2 | [`ERROS_COMUNS.md`](ERROS_COMUNS.md) | **todos os erros que costumam cair** e como corrigir | 15 min |
| 3 | [`exercicios_corrigir/`](exercicios_corrigir/) | 6 códigos com erros para você consertar + gabarito | 30–60 min |
| 4 | [`GUIA_TEORIA.md`](GUIA_TEORIA.md) | conceitos de estatística, boxplot, ETL, falas para as personas | 20 min |
| 5 | [`aulas/`](aulas/) | aulas em código, comentadas linha a linha | o resto do tempo |
| 6 | [`dashboard/`](dashboard/) | dashboard Streamlit completo (modelo de trabalho nota máxima) | |

### As aulas (rode cada uma e leia junto com a saída)
| Arquivo | Conteúdo |
|---|---|
| `aulas/01_python_basico.py` | variáveis, tipos, listas, dicionários, if, for, funções, try/except, tipos de erro |
| `aulas/02_pandas_etl.py` | ler CSV/XLSX, filtrar, groupby, pivot, **limpar base suja do IBGE**, melt, merge |
| `aulas/03_estatistica.py` | média, mediana, moda, amplitude, variância, desvio, quartis, IQR, **outliers**: na mão × Pandas × NumPy |
| `aulas/04_graficos.py` | barras, boxplot, linha, histograma, pizza, scatter, 100%, pirâmide, radar (e quando usar cada um) |
| `dashboard/app.py` | aula 05: Streamlit completo com menu, upload, filtros, KPIs, estatística, gráficos, notícias |

### Exercícios de corrigir código
| Exercício | Tema | Erros |
|---|---|---|
| `ex01_python_basico.py` | sintaxe, indentação, tipos, return | 7 |
| `ex02_estatistica_manual.py` | fórmulas na mão (erros de lógica!) | 7 |
| `ex03_pandas_etl.py` | leitura do CSV do IBGE, filtros, groupby | 8 |
| `ex04_quartis_outliers.py` | quantile, IQR, limites, outliers, std × var | 7 |
| `ex05_graficos.py` | Plotly | 6 |
| `ex06_streamlit_app.py` | app Streamlit inteiro | 9 |

Gabaritos comentados em `exercicios_corrigir/gabarito/`, com uma tabela no topo de cada arquivo listando **cada erro, o sintoma e a correção**.
**Tente sozinho primeiro!**

---

## ▶️ Como rodar

```bash
# 1. instalar as bibliotecas (uma vez só)
pip install -r requirements.txt

# 2. (opcional) recriar as bases de exemplo
python dados/gerar_dados.py

# 3. rodar uma aula (sempre a partir da pasta do projeto)
python aulas/03_estatistica.py

# 4. rodar o dashboard
streamlit run dashboard/app.py
```

## 📁 Estrutura

```
├── COLA.md                  resumo de 1 página
├── ERROS_COMUNS.md          catálogo de erros + checklist
├── GUIA_TEORIA.md           teoria + roda de conversa
├── requirements.txt         bibliotecas
├── dados/
│   ├── gerar_dados.py       cria as bases fictícias
│   ├── afazeres_domesticos.csv        base limpa
│   ├── afazeres_domesticos_sujo.csv   base "suja" (formato IBGE) para treinar ETL
│   └── desocupacao_uf.csv             desemprego por UF 2012 × 2022
├── aulas/                   01 a 04, comentadas
├── dashboard/
│   ├── app.py               painel integrado (menu lateral)
│   └── modulos/
│       ├── estatistica.py   funções compartilhadas (resumo estatístico, leitura de arquivo)
│       ├── afazeres.py      página individual: persona 1
│       └── desocupacao.py   página individual: persona 6
└── exercicios_corrigir/     6 exercícios + gabarito/
```

## 🎯 Como a rubrica do trabalho se liga a este material

| Critério | Pontos | Onde estudar |
|---|---|---|
| 1. ETL, upload e filtros | 0,75 | `aulas/02`, `dashboard/modulos/afazeres.py` (partes 1 e 2), `ex03`, `ex06` |
| 2. Rigor estatístico + perguntas de negócio | 0,90 | `aulas/03`, `GUIA_TEORIA.md §3`, `ex02`, `ex04` |
| 3. Visualização + mídias | 0,60 | `aulas/04`, `ex05`, seção de notícias do dashboard |
| 4. Apresentação (roda de conversa) | 0,75 | `GUIA_TEORIA.md §6` |
