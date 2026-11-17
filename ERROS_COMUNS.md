# 🐞 Guia de Caça aos Erros (para a prova de corrigir código)

## Método em 5 passos

1. **Rode o código.** Não tente achar tudo só lendo.
2. **Leia a ÚLTIMA linha do erro.** Ela diz o **tipo** (`KeyError`, `TypeError`...) e a mensagem.
   Logo acima vem `File "...", line 23`: é a **linha** do problema.
3. **Corrija um erro só e rode de novo.** O Python para no primeiro erro, então o próximo só aparece depois.
4. **Quando parar de dar erro, confira o resultado.** Erros de **lógica** não mostram mensagem nenhuma: a conta só sai errada (média dividindo por n-1, filtro que não filtra, gráfico usando `df` em vez de `filtrado`).
5. **Comente o que corrigiu.** Ex.: `# CORRIGIDO: faltava ":"`. Isso mostra ao professor que você entendeu.

> 💡 Se não puder rodar (prova no papel), leia linha por linha procurando os itens da checklist abaixo.

---

## 1. Erros de Python básico

| Erro (mensagem) | Causa típica | Como corrigir |
|---|---|---|
| `SyntaxError: expected ':'` | faltou `:` no `def`, `if`, `elif`, `else`, `for`, `while` | adicionar `:` |
| `SyntaxError: invalid syntax` com `=` | usou `=` (atribuição) no lugar de `==` (comparação) | `if x == 10:` |
| `SyntaxError: '(' was never closed` | parêntese, colchete ou aspas sem fechar | conte os pares `()` `[]` `""` |
| `IndentationError: expected an indented block` | corpo do `if`/`for`/`def` sem os 4 espaços | indentar |
| `IndentationError: unexpected indent` | espaço sobrando no começo da linha | alinhar |
| `NameError: name 'pd' is not defined` | faltou `import pandas as pd` | importar |
| `NameError: name 'meida' is not defined` | erro de digitação na variável | corrigir o nome |
| `TypeError: can only concatenate str (not "float") to str` | `"Média: " + 10.5` | `f"Média: {valor}"` ou `str(valor)` |
| `TypeError: unsupported operand type(s) for /: 'NoneType'...` | função sem `return` devolve `None` | colocar `return` |
| `TypeError: 'int' object is not callable` | parênteses onde não deve, ex.: `df.shape()` | `df.shape` (é atributo) |
| `ValueError: could not convert string to float: '21,5'` | vírgula decimal | `.replace(",", ".")` ou `decimal=","` |
| `IndexError: list index out of range` | posição que não existe | lembrar que começa em 0 e vai até `len-1` |
| `KeyError: 'BA'` | chave/coluna não existe | conferir o nome exato (maiúsculas!) |
| `ZeroDivisionError` | dividiu por zero (lista vazia) | checar `if len(x) > 0` |
| `ModuleNotFoundError: No module named 'plotly'` | biblioteca não instalada | `pip install plotly` |
| `FileNotFoundError` | caminho do arquivo errado | conferir pasta / rodar da pasta certa |

## 2. Erros de Pandas

| Erro / sintoma | Causa | Correção |
|---|---|---|
| `KeyError: 'Sexo'` | nome da coluna diferente (`sexo`) ou com espaço (`"sexo "`) | `print(df.columns)` e usar o nome exato; `df.columns = df.columns.str.strip()` |
| `ValueError: The truth value of a Series is ambiguous` | usou `and`/`or` entre condições | `&` / `\|` **com parênteses**: `df[(a) & (b)]` |
| `TypeError: unsupported operand type(s) for &` | faltaram parênteses: `df["a"] == 1 & df["b"] == 2` | `(df["a"] == 1) & (df["b"] == 2)` |
| `TypeError: isin() takes 2 positional arguments...` | `.isin("BA", "PE")` | `.isin(["BA", "PE"])` (lista) |
| `UnicodeDecodeError: 'utf-8' codec can't decode` | arquivo em latin-1 | `encoding="latin-1"` |
| Tudo numa coluna só / `ParserError` | separador errado | `sep=";"` |
| Coluna numérica com `dtype object` | `"21,5"`, `"..."`, `"-"` | `decimal=","`, `na_values=["...","-"]`, `pd.to_numeric(..., errors="coerce")` |
| `TypeError: can't multiply sequence...` / média de texto | coluna é texto | converter com `pd.to_numeric` / `astype(float)` |
| **Nada muda** depois de `df.dropna()` | não atribuiu | `df = df.dropna()` (ou `inplace=True`) |
| `<bound method ...>` aparece no lugar do número | esqueceu `()` | `.mean()`, `.median()`, `.std()` |
| `ValueError: percentiles should all be in the interval [0, 1]` | `quantile(25)` | `quantile(0.25)` |
| Filtro devolve **tabela vazia** | texto com espaço/minúscula (`" ba"`) ou tipo errado (`"2022"` x `2022`) | `.str.strip().str.upper()`; `astype(int)` |
| `SettingWithCopyWarning` | modificou uma fatia de outro df | `filtrado = df[...].copy()` |
| groupby resultando em índice estranho no gráfico | faltou `reset_index()` / `as_index=False` | `df.groupby("uf", as_index=False)["x"].mean()` |

## 3. Erros de estatística (lógica: não aparece mensagem!)

| Errado | Certo |
|---|---|
| média = `sum(x) / (len(x) - 1)` | `sum(x) / len(x)` |
| mediana sem ordenar | `sorted(x)` antes |
| mediana com n par usando `v[meio]` e `v[meio+1]` | `(v[meio-1] + v[meio]) / 2` |
| moda com `min(...)` | `max(contagem, key=contagem.get)` |
| amplitude = `min - max` | `max - min` |
| variância sem elevar ao quadrado | `sum((x - m) ** 2 ...)` |
| desvio padrão = variância `** 2` | `variância ** 0.5` (**raiz**) |
| confundir `.std()` com `.var()` | desvio = `.std()`; variância = `.var()` |
| `IQR = Q1 - Q3` | `IQR = Q3 - Q1` |
| limite com `1.5 * Q1` | `Q1 - 1.5*IQR` e `Q3 + 1.5*IQR` |
| outlier com `&` (fica sempre vazio) | `(x < li) \| (x > ls)` |
| `np.percentile(x, 0.25)` | `np.percentile(x, 25)` (numpy usa 0–100) |
| `s.quantile(25)` | `s.quantile(0.25)` (pandas usa 0–1) |
| "média > mediana = assimetria à esquerda" | média > mediana = assimetria à **direita** (positiva) |
| pandas `s.std()` ≠ numpy `np.std(x)` e achar que é bug | pandas usa **n-1** (amostral), numpy usa **n** (populacional). Igualar com `ddof` |

## 4. Erros de gráficos (Plotly / Matplotlib)

| Erro | Correção |
|---|---|
| `px.boxplot` → `AttributeError` | `px.box` |
| `px.histogram(..., bins=20)` | `nbins=20` |
| `label={...}` | `labels={...}` |
| `barmode="grouped"` | `barmode="group"` |
| `x="UF"` → `ValueError: Value of 'x' is not the name of a column` | usar o nome exato da coluna |
| `px.pie(df, x=..., y=...)` | `px.pie(df, names="categoria", values="valor")` |
| Linha "rabiscada" | agrupar por ano antes do `px.line` e ordenar por ano |
| `st.pyplot(fig_plotly)` | Plotly → `st.plotly_chart(fig)`; Matplotlib → `st.pyplot(fig)` |
| `plt.show()` dentro do Streamlit | usar `st.pyplot(fig)` |
| `fig.show` sem `()` | `fig.show()` |

## 5. Erros de Streamlit

| Erro / sintoma | Correção |
|---|---|
| Rodou com `python app.py` e nada abriu | `streamlit run app.py` |
| `set_page_config` depois de outro `st.` | colocar como **primeiro** comando |
| `ValueError: Invalid file path or buffer object type: <class 'NoneType'>` | `file_uploader` devolve `None` até o usuário enviar: `if arquivo is not None:` |
| Upload de `.xlsx` lido com `read_csv` | `if arquivo.name.endswith(".xlsx"): pd.read_excel(arquivo)` |
| `StreamlitAPIException: ... default value ... not part of the options` | o `default` do multiselect tem que estar nas opções |
| `DuplicateWidgetID` | dois widgets iguais → dar `key="..."` diferente |
| **Filtro não muda o gráfico** | gráfico/KPI usando `df` em vez de `filtrado` |
| Filtro fora da barra lateral | `st.sidebar.multiselect(...)` (não `st.multiselect`) |
| Slider de intervalo comparando `anos[0]` duas vezes | slider com tupla devolve `(inicio, fim)` → usar `anos[0]` e `anos[1]` |
| Filtro vazio quebra o app | `if filtrado.empty: st.warning(...); st.stop()` |
| `st.metric("Média", serie.mean)` | `f"{serie.mean():.1f}"` |
| `st.columns(3)` e usar `c4` | criar a quantidade certa de colunas |
| App lento relendo arquivo a cada clique | `@st.cache_data` na função de leitura |
| Imagem não aparece | caminho errado / URL quebrada → `st.image("pasta/arquivo.png")` |

## Checklist rápida para ler um código suspeito

- [ ] Todos os `import` existem e com o apelido certo (`pd`, `np`, `st`, `px`)?
- [ ] Todo `def/if/for/else` tem `:` e o corpo indentado?
- [ ] Comparações usam `==`?
- [ ] Nomes de colunas batem **exatamente** com o arquivo?
- [ ] `read_csv` tem `sep`, `decimal`, `encoding` adequados?
- [ ] Métodos do pandas atribuídos (`df = df.dropna()`)? Têm `()`?
- [ ] Filtros com `&`/`|` e parênteses? `isin` com lista?
- [ ] Fórmulas: média /n, mediana ordenada, IQR = Q3−Q1, limites com 1,5·IQR, outlier com `|`, desvio = raiz?
- [ ] Gráficos e KPIs usam o DataFrame **filtrado**?
- [ ] `file_uploader` checa `None`? Filtro vazio tem `st.stop()`?
- [ ] Função de plotly certa (`px.box`, `nbins`, `labels`) e exibida com `st.plotly_chart`?
