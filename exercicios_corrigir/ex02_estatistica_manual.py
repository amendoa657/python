"""
EXERCÍCIO 02 — Estatística "na mão" (sem Pandas)        (7 erros)
-----------------------------------------------------------------
Todos os erros aqui são de LÓGICA/MATEMÁTICA: o código RODA, mas
os resultados saem ERRADOS. Você precisa saber as fórmulas!

Dados: [12, 5, 9, 7, 20, 7, 10, 8]   (n = 8, número PAR)

Saída esperada:
    Média: 9.75
    Mediana: 8.5
    Moda: 7
    Amplitude: 15
    Variância (populacional): 18.94
    Desvio padrão (populacional): 4.35

Gabarito: exercicios_corrigir/gabarito/ex02_estatistica_manual.py
"""

dados = [12, 5, 9, 7, 20, 7, 10, 8]


def media(v):
    return sum(v) / (len(v) - 1)


def mediana(v):
    n = len(v)
    meio = n // 2
    if n % 2 == 1:
        return v[meio]
    return (v[meio] + v[meio + 1]) / 2


def moda(v):
    contagem = {}
    for x in v:
        contagem[x] = contagem.get(x, 0) + 1
    return min(contagem, key=contagem.get)


def amplitude(v):
    return min(v) - max(v)


def variancia(v):
    m = media(v)
    return sum((x - m) for x in v) / len(v)


def desvio_padrao(v):
    return variancia(v) ** 2


print(f"Média: {media(dados):.2f}")
print(f"Mediana: {mediana(dados)}")
print(f"Moda: {moda(dados)}")
print(f"Amplitude: {amplitude(dados)}")
print(f"Variância (populacional): {variancia(dados):.2f}")
print(f"Desvio padrão (populacional): {desvio_padrao(dados):.2f}")
