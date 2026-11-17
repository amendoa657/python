"""
=============================================================================
AULA 01 — PYTHON BÁSICO (o mínimo que você PRECISA saber para a prova)
=============================================================================
Como rodar:  python aulas/01_python_basico.py
Leia o código DE CIMA PARA BAIXO junto com o que aparece no terminal.

Tudo que vem depois de # é COMENTÁRIO: o Python ignora. Serve para explicar.
Textos entre três aspas (como este) são "docstrings": também são explicação.
=============================================================================
"""

# ---------------------------------------------------------------------------
# 1. VARIÁVEIS E TIPOS
# ---------------------------------------------------------------------------
# Variável = uma "caixinha" com nome que guarda um valor. Cria com  =
nome = "Bahia"          # str   (string = texto) -> SEMPRE entre aspas
ano = 2022              # int   (número inteiro)
horas = 21.5            # float (número com casa decimal) -> usa PONTO, não vírgula!
eh_nordeste = True      # bool  (True ou False, com letra MAIÚSCULA)

print("=== 1. Variáveis ===")
print(nome, ano, horas, eh_nordeste)
print(type(horas))      # type() diz o tipo -> <class 'float'>

# ERRO CLÁSSICO: misturar texto com número.
# print("Ano: " + ano)          -> TypeError: can only concatenate str (not "int") to str
print("Ano: " + str(ano))       # solução 1: converter com str()
print(f"Ano: {ano}")            # solução 2 (melhor): f-string -> f"...{variavel}..."
print(f"Horas com 2 casas: {horas:.2f}")   # :.2f = formata com 2 casas decimais

# Conversões úteis
print(int("2022") + 1)          # texto -> inteiro
print(float("21.5") * 2)        # texto -> decimal
# float("21,5")  -> ValueError! O Python NÃO entende vírgula decimal.
print(float("21,5".replace(",", ".")))   # troca vírgula por ponto antes

# ---------------------------------------------------------------------------
# 2. OPERADORES
# ---------------------------------------------------------------------------
print("\n=== 2. Operadores ===")
print(7 + 2, 7 - 2, 7 * 2)  # soma, subtração, multiplicação
print(7 / 2)    # 3.5  divisão normal (sempre dá float)
print(7 // 2)   # 3    divisão inteira (corta a parte decimal)
print(7 % 2)    # 1    resto da divisão (bom para saber se é par: n % 2 == 0)
print(7 ** 2)   # 49   potência (7 ao quadrado). Raiz quadrada: 49 ** 0.5

# Comparação -> devolvem True/False
#   ==  igual (DOIS sinais!)   !=  diferente   >  <  >=  <=
# ERRO CLÁSSICO: usar  =  (atribuição) quando queria  ==  (comparação)
print(ano == 2022, ano != 2022, horas >= 20)

# Lógicos: and (E), or (OU), not (NÃO)
print(horas > 20 and eh_nordeste)

# ---------------------------------------------------------------------------
# 3. LISTAS  [ ]  -> sequência ordenada de valores
# ---------------------------------------------------------------------------
print("\n=== 3. Listas ===")
horas_estados = [21.5, 19.8, 23.1, 18.0, 22.4]
print(horas_estados[0])     # primeiro elemento -> índice 0 (Python começa no ZERO!)
print(horas_estados[-1])    # último elemento
print(horas_estados[1:3])   # "fatia": do índice 1 ATÉ o 3 (o 3 NÃO entra) -> [19.8, 23.1]
print(len(horas_estados))   # quantidade de elementos -> 5
print(sum(horas_estados), min(horas_estados), max(horas_estados))
horas_estados.append(20.0)  # adiciona no final
print(sorted(horas_estados))  # devolve uma cópia ordenada
# ERRO CLÁSSICO: horas_estados[6] -> IndexError (só existem índices 0 a 5)

# ---------------------------------------------------------------------------
# 4. DICIONÁRIOS  { chave: valor }
# ---------------------------------------------------------------------------
print("\n=== 4. Dicionários ===")
regiao_de = {"BA": "Nordeste", "SP": "Sudeste", "AM": "Norte"}
print(regiao_de["BA"])              # acessa pela CHAVE -> "Nordeste"
regiao_de["RS"] = "Sul"             # adiciona/atualiza
print(regiao_de.get("XX", "???"))   # .get não dá erro se a chave não existe
# regiao_de["XX"] -> KeyError (chave não existe)  ← erro comum também no Pandas!
for uf, reg in regiao_de.items():   # percorre chave e valor
    print(f"  {uf} fica no {reg}")

# ---------------------------------------------------------------------------
# 5. IF / ELIF / ELSE  (decisão)
# ---------------------------------------------------------------------------
# A INDENTAÇÃO (4 espaços) define o que está "dentro" do if. Não esqueça os  :
print("\n=== 5. if/elif/else ===")
taxa = 14.2
if taxa >= 12:
    print("Desemprego ALTO")
elif taxa >= 8:          # elif = "senão, se..."
    print("Desemprego MÉDIO")
else:
    print("Desemprego BAIXO")

# ---------------------------------------------------------------------------
# 6. FOR e WHILE  (repetição)
# ---------------------------------------------------------------------------
print("\n=== 6. Laços ===")
for h in horas_estados:          # para cada valor h dentro da lista...
    print("  ", h)

for i in range(3):               # range(3) gera 0, 1, 2
    print("  volta", i)

total = 0
for h in horas_estados:          # padrão "acumulador" (muito usado!)
    total = total + h            # ou: total += h
media_manual = total / len(horas_estados)
print(f"Média calculada na mão: {media_manual:.2f}")

contador = 0
while contador < 3:              # repete ENQUANTO a condição for verdadeira
    contador += 1                # se esquecer isso -> laço infinito!
print("contador terminou em", contador)

# "List comprehension": cria lista nova em 1 linha
altas = [h for h in horas_estados if h > 20]
print("Acima de 20h:", altas)

# ---------------------------------------------------------------------------
# 7. FUNÇÕES  (def)
# ---------------------------------------------------------------------------
# Função = bloco de código com nome, que recebe entradas (parâmetros)
# e devolve uma saída com  return.
print("\n=== 7. Funções ===")

def calcular_media(valores):
    """Recebe uma lista de números e devolve a média aritmética."""
    if len(valores) == 0:        # proteção contra divisão por zero
        return 0
    return sum(valores) / len(valores)

def classificar(taxa, limite=10):    # limite=10 -> parâmetro com valor PADRÃO
    return "acima" if taxa > limite else "abaixo"

print(calcular_media([10, 20, 30]))   # 20.0
print(classificar(12), classificar(12, limite=15))
# ERRO CLÁSSICO: esquecer o return -> a função devolve None
# ERRO CLÁSSICO: chamar sem parênteses -> calcular_media (isso é a função, não o resultado)

# ---------------------------------------------------------------------------
# 8. IMPORT  (usar bibliotecas)
# ---------------------------------------------------------------------------
# import biblioteca as apelido   <- apelidos PADRÃO que todo mundo usa:
#   import pandas as pd
#   import numpy as np
#   import streamlit as st
#   import plotly.express as px
#   import matplotlib.pyplot as plt
# ERRO CLÁSSICO: usar pd.read_csv sem ter feito "import pandas as pd" -> NameError
import statistics
print("\n=== 8. import ===")
print("mediana com statistics:", statistics.median([3, 1, 2]))

# ---------------------------------------------------------------------------
# 9. TRATAMENTO DE ERROS  (try / except)
# ---------------------------------------------------------------------------
print("\n=== 9. try/except ===")
for texto in ["21.5", "...", "18"]:
    try:
        print("  convertido:", float(texto))
    except ValueError:              # se der ValueError, cai aqui em vez de quebrar
        print(f"  '{texto}' não é número, ignorando")

# ---------------------------------------------------------------------------
# RESUMO DOS ERROS QUE O PYTHON MOSTRA (leia a ÚLTIMA linha do erro!)
# ---------------------------------------------------------------------------
#  SyntaxError       -> escreveu errado: faltou  :  )  ]  aspas, ou usou = no lugar de ==
#  IndentationError  -> espaços/tab errados no começo da linha
#  NameError         -> variável/função/biblioteca não existe (erro de digitação? faltou import?)
#  TypeError         -> tipo errado (somar texto + número, chamar algo que não é função)
#  ValueError        -> tipo certo mas valor inválido (float("abc"), float("21,5"))
#  KeyError          -> chave/coluna não existe (dicionário ou df["coluna_errada"])
#  IndexError        -> posição fora da lista
#  ZeroDivisionError -> dividiu por zero
#  ModuleNotFoundError -> biblioteca não instalada -> pip install nome
#  FileNotFoundError -> caminho do arquivo errado
print("\nFim da aula 01!")
