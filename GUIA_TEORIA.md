# 📘 Guia de Teoria: "Números que Falam"

Este guia explica **o que** é cada coisa e **por que** se faz assim. O código de cada parte está em `aulas/`.

---

## 0. O que é o projeto, em uma frase

> Pegar uma tabela do **IBGE**, **limpar** com Pandas (ETL), **calcular estatísticas** (média, mediana, quartis, IQR, desvio padrão, outliers), **mostrar** num **dashboard Streamlit** com filtros e gráficos, e **explicar** os números para um gestor público (persona) como se você fosse uma startup de dados.

| Pilar | O que fazer | Ferramenta | Peso na rubrica |
|---|---|---|---|
| 1. ETL e interface | upload CSV/XLSX, limpeza, filtros na barra lateral | Pandas + Streamlit | 0,75 |
| 2. Estatística | média, mediana, moda, quartis, IQR, amplitude, DP, outliers + responder perguntas | Pandas/NumPy | **0,90** |
| 3. Visualização | barras, boxplot (+ linha, histograma...), notícias e imagens | Plotly + Streamlit | 0,60 |
| 4. Apresentação | falar como consultor, ligar número → decisão | você | 0,75 |

---

## 1. As ferramentas

| Ferramenta | O que é | Analogia |
|---|---|---|
| **Python** | linguagem de programação | a língua que você fala com o computador |
| **Pandas** (`pd`) | biblioteca de tabelas (DataFrame) | Excel dentro do Python |
| **NumPy** (`np`) | biblioteca de cálculo numérico | calculadora científica |
| **Plotly Express** (`px`) | gráficos interativos | gerador de gráficos do Excel, só que interativo |
| **Matplotlib** (`plt`) | gráficos estáticos (mais antigo) | idem, sem interação |
| **Streamlit** (`st`) | transforma um script Python em site/dashboard | PowerPoint interativo feito com código |
| **SIDRA** | site do IBGE de onde se baixam as tabelas | o "banco de dados" público |
| `requirements.txt` | lista das bibliotecas do projeto | lista de ingredientes. Instala com `pip install -r requirements.txt` |

---

## 2. ETL (Extract, Transform, Load)

**Extract (extrair):** ler o arquivo.
- `pd.read_csv("arq.csv")` / `pd.read_excel("arq.xlsx")`
- No Streamlit: `arquivo = st.file_uploader(...)` e depois `pd.read_csv(arquivo)`

**Transform (transformar/limpar):** o arquivo do IBGE quase nunca vem pronto.

| Problema | Solução |
|---|---|
| `;` como separador | `sep=";"` |
| `21,5` (vírgula decimal) | `decimal=","` |
| acentos quebrados | `encoding="latin-1"` |
| linhas de título no topo | `skiprows=N` |
| `...`, `-`, `X` no lugar de número | `na_values=["...", "-", "X"]` |
| nomes de coluna feios | `df.rename(columns={...})` |
| espaços/maiúsculas (" ba") | `.str.strip().str.upper()` |
| valores faltando (NaN) | `dropna()` ou `fillna(mediana)` |
| linhas repetidas | `drop_duplicates()` |
| texto que deveria ser número | `pd.to_numeric(col, errors="coerce")` |

**Load (carregar):** salvar a base limpa (`df.to_csv("tratado.csv", index=False)`) e usar no dashboard.

> 🎤 **Como explicar:** "Os dados do IBGE vêm com separador `;`, vírgula decimal e símbolos como '...' para dados ausentes. No ETL padronizamos os nomes, convertemos os tipos, removemos ausentes e duplicados. Só depois calculamos as estatísticas, senão a média sairia errada."

---

## 3. Estatística descritiva: conceito, cálculo e interpretação

Exemplo usado: `[6, 7, 7, 8, 9, 10, 11, 12, 30]` (desemprego % de 9 estados; o 30 é outlier).

### Tendência central ("qual é o valor típico?")

| Medida | Como calcula | Resultado | Quando usar |
|---|---|---|---|
| **Média** | soma ÷ quantidade | 100/9 = **11,11** | dados simétricos, sem outliers |
| **Mediana** | ordena e pega o do meio (n par: média dos 2 do meio) | **9** | quando há outliers ou assimetria (renda!) |
| **Moda** | valor que mais aparece | **7** | dados categóricos ("modal mais usado") |

**Por que a média deu 11 e a mediana 9?** Porque o 30 "puxa" a média para cima. A mediana não liga para o quão extremo é o valor, só para a posição.

### Dispersão ("os dados são parecidos ou espalhados?")

| Medida | Como calcula | Resultado | Interpretação |
|---|---|---|---|
| **Amplitude** | máx − mín | 30 − 6 = **24** | distância entre o melhor e o pior estado |
| **Variância** | média dos (x − média)² | 54,11 (amostral) | unidade ao quadrado, difícil de interpretar |
| **Desvio padrão** | √variância | **7,36** | "em média, os estados se afastam 7,4 p.p. da média" |
| **Quartis** | dividem os dados ordenados em 4 partes | Q1=7, Q2=9, Q3=11 | 25% abaixo de Q1, 50% abaixo de Q2, 75% abaixo de Q3 |
| **IQR** | Q3 − Q1 | 11 − 7 = **4** | espalhamento dos 50% do meio (resistente a outliers) |
| **CV** (bônus) | DP ÷ média × 100 | 66% | > 30% = alta dispersão |

- **Desvio padrão pequeno** → estados **homogêneos** (parecidos). **Grande** → **heterogêneos** (desigualdade regional).
- **Amostral (n−1) × populacional (n):** Pandas `.std()` usa n−1; NumPy `np.std()` usa n. Os dois estão certos, são convenções diferentes. Saiba explicar a diferença.

### Outliers: regra do 1,5 × IQR (Tukey)

```
Limite inferior = Q1 − 1,5 × IQR = 7 − 6 = 1
Limite superior = Q3 + 1,5 × IQR = 11 + 6 = 17
→ 30 > 17  →  30 é OUTLIER
```

**Impacto:** com o 30, média = 11,11 e mediana = 9. Sem o 30, média = 8,75 e mediana = 8,5. A média mudou muito e a mediana quase nada. **Conclusão: com outliers, use a mediana.**

**Outlier não é erro automaticamente!** Pode ser erro de digitação (aí corrige ou remove) ou um caso real e importante (ex.: uma cidade que cresceu muito por causa de uma indústria). **Investigue e justifique**, porque é isso que a rubrica pede.

### Assimetria (comparando média e mediana)

| Situação | Nome | Exemplo |
|---|---|---|
| média > mediana | assimetria **positiva / à direita** (cauda de valores altos) | renda: poucos muito ricos puxam a média |
| média < mediana | assimetria **negativa / à esquerda** | nota de prova fácil: quase todos tiram nota alta |
| média ≈ mediana | simétrica | altura das pessoas |

### Como ler um BOXPLOT

```
      o          ← outlier (ponto acima do limite superior)
      |
   ───┬───       ← fim do bigode = maior valor NÃO outlier
      |
   ┌──┴──┐       ← Q3 (75%)
   │     │
   ├─────┤       ← MEDIANA (Q2)
   │     │
   └──┬──┘       ← Q1 (25%)      altura da caixa = IQR
      |
   ───┴───       ← fim do bigode = menor valor NÃO outlier
```
- Caixa **alta** = muita dispersão; caixa **baixa** = dados concentrados.
- Mediana **mais perto do fundo** da caixa = cauda para cima (assimetria à direita).
- Comparar caixas lado a lado (homens × mulheres) mostra desigualdade **visualmente**.

---

## 4. Qual gráfico usar

| Pergunta | Gráfico |
|---|---|
| Comparar estados/grupos | **Barras** (agrupadas: `barmode="group"`) |
| Dispersão, quartis e outliers | **Boxplot** |
| Evolução no tempo | **Linha** |
| Forma da distribuição, média × mediana | **Histograma** |
| Partes de um todo (poucas categorias) | **Pizza/rosca** |
| Relação entre duas variáveis numéricas | **Dispersão (scatter)** |
| Proporção de gênero por área | **Barras 100% empilhadas** |
| Estrutura etária | **Pirâmide etária** |
| Comparar subíndices (IDH) | **Radar** |

Sempre com **título** e **rótulos nos eixos** (a rubrica tira ponto se faltar).

---

## 5. Streamlit em 1 minuto

1. O script roda **inteiro, de cima a baixo**, a cada interação.
2. Cada widget **devolve um valor**: `ufs = st.sidebar.multiselect(...)`.
3. Você filtra o DataFrame com esse valor: `filtrado = df[df["uf"].isin(ufs)]`.
4. Tudo que vem depois (KPIs, gráficos) usa `filtrado`, e por isso "muda quando mexe no filtro".
5. Roda com `streamlit run app.py`.

Estrutura típica de uma página:

```python
st.set_page_config(...)                       # 1º comando
arquivo = st.sidebar.file_uploader(...)       # upload
df = pd.read_csv(arquivo) if arquivo else pd.read_csv("padrao.csv")
ufs = st.sidebar.multiselect(...)             # filtros
filtrado = df[df["uf"].isin(ufs)]
if filtrado.empty: st.warning("..."); st.stop()
c1, c2 = st.columns(2); c1.metric("Média", f"{filtrado['x'].mean():.1f}")   # KPIs
st.plotly_chart(px.bar(...)); st.plotly_chart(px.box(...))                   # gráficos
st.markdown("[Notícia](https://...)"); st.image("img.png")                    # mídia
```

---

## 6. Roda de conversa: o que falar para cada persona

**Fórmula de resposta de consultor (use sempre):**
> **Número** → **Significado** → **Decisão**
> "A mediana é X (número). Isso significa que metade dos estados está acima de X (significado). Recomendamos priorizar os estados acima do Q3 (decisão)."

| # | Indicador / Persona | Métricas-chave | Frase-modelo |
|---|---|---|---|
| 1 | **Afazeres domésticos** — Secretárias BA, PE, AM, CE | diferença de horas M−H por UF; por raça; ocupadas × desocupadas | "As mulheres dedicam ~11h a mais por semana; mulheres pretas/pardas, ainda mais. Sugerimos creches e licença parental compartilhada onde a diferença passa do Q3." |
| 2 | **Curso superior** — Governadores do Sudeste | % com superior por UF; evolução; % de mulheres em Exatas × Humanas | "Mulheres são minoria em Exatas; programas de bolsas STEM para mulheres ampliam o banco de talentos." |
| 3 | **Crescimento demográfico** — Prefeitos de capitais | taxa de crescimento por cidade; outliers (cresceu muito / encolheu); envelhecimento | "Cidades acima do limite superior precisam de infraestrutura; as que encolhem e envelhecem precisam de saúde do idoso." |
| 4 | **IDH/IDHM** — Consórcio de governadores | dimensão mais baixa (Longevidade/Educação/Renda); evolução desde 2000; IQR/DP entre municípios | "Em MA e PA a Educação puxa o IDH para baixo, então o fundo deve priorizar educação básica. O IQR alto mostra desigualdade interna." |
| 5 | **Transporte** — Secretaria de Mobilidade | mediana do tempo de deslocamento por raça; % público × privado × ativo; boxplot com gargalos | "A mediana do tempo de deslocamento de pessoas negras é maior: elas moram mais longe e dependem de ônibus. Investir em corredores de ônibus." |
| 6 | **Trabalho** — Ministra, Indústria, Sebrae | desocupação 2012 × 2022 por UF e sexo; maior redução; informalidade; média × mediana da renda | "A renda média é maior que a mediana (assimetria à direita): a maioria ganha menos que a média. Use a mediana para desenhar políticas." |

**Perguntas que o professor pode fazer, com respostas curtas:**
- *Por que usar a mediana e não a média?* Porque há outliers/assimetria; a mediana é robusta.
- *O que é o IQR?* Q3 − Q1: espalhamento dos 50% centrais, base para detectar outliers.
- *Como você detectou outliers?* Regra 1,5×IQR: abaixo de Q1−1,5·IQR ou acima de Q3+1,5·IQR.
- *Desvio padrão alto significa o quê?* Estados muito diferentes entre si (heterogeneidade/desigualdade).
- *Diferença entre variância e desvio padrão?* Desvio = raiz da variância; está na mesma unidade dos dados.
- *Por que seus filtros funcionam?* Os widgets devolvem valores usados para filtrar o DataFrame; gráficos usam o DataFrame filtrado.
- *O que você fez no ETL?* Ajustei separador/decimal/encoding, renomeei colunas, tratei "..."/"-" como ausentes, removi nulos e duplicados, padronizei textos.
