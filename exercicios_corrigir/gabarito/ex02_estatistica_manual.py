"""
GABARITO 02 — Estatística na mão (7 erros, todos de LÓGICA)

 #  Onde               Erro                                   Correção
 1  media              divide por (n - 1)                     média divide por n
 2  mediana            não ORDENA os dados antes              v = sorted(v)
 3  mediana (par)      usa v[meio] e v[meio+1]                os dois do meio são v[meio-1] e v[meio]
 4  moda               min(...) pega o MENOS frequente        max(...) pega o MAIS frequente
 5  amplitude          min - max (dá negativo)                max - min
 6  variancia          esqueceu de elevar ao QUADRADO         (x - m) ** 2
 7  desvio_padrao      elevou ao quadrado (** 2)              desvio = RAIZ da variância -> ** 0.5

Conta na mão para conferir:
  ordenados: [5, 7, 7, 8, 9, 10, 12, 20]
  média = 78 / 8 = 9.75
  mediana (n par) = (8 + 9) / 2 = 8.5        <- 4º e 5º elementos (índices 3 e 4)
  moda = 7 (aparece 2x)
  amplitude = 20 - 5 = 15
  desvios²: 22.56, 7.56, 7.56, 3.06, 0.56, 0.06, 5.06, 105.06 -> soma 151.5
  variância pop = 151.5 / 8 = 18.94
  desvio pop = raiz(18.94) = 4.35
"""

dados = [12, 5, 9, 7, 20, 7, 10, 8]


def media(v):
    return sum(v) / len(v)                     # CORRIGIDO (1)


def mediana(v):
    v = sorted(v)                              # CORRIGIDO (2): ordenar primeiro!
    n = len(v)
    meio = n // 2
    if n % 2 == 1:
        return v[meio]
    return (v[meio - 1] + v[meio]) / 2         # CORRIGIDO (3)


def moda(v):
    contagem = {}
    for x in v:
        contagem[x] = contagem.get(x, 0) + 1
    return max(contagem, key=contagem.get)     # CORRIGIDO (4)


def amplitude(v):
    return max(v) - min(v)                     # CORRIGIDO (5)


def variancia(v):
    m = media(v)
    return sum((x - m) ** 2 for x in v) / len(v)   # CORRIGIDO (6): ao quadrado
    # amostral seria: / (len(v) - 1)


def desvio_padrao(v):
    return variancia(v) ** 0.5                 # CORRIGIDO (7): raiz quadrada
    # ou: import math; math.sqrt(variancia(v))


print(f"Média: {media(dados):.2f}")
print(f"Mediana: {mediana(dados)}")
print(f"Moda: {moda(dados)}")
print(f"Amplitude: {amplitude(dados)}")
print(f"Variância (populacional): {variancia(dados):.2f}")
print(f"Desvio padrão (populacional): {desvio_padrao(dados):.2f}")
