"""
EXERCÍCIO 01 — Python básico            (7 erros)
-----------------------------------------------------------------
Objetivo do programa: dada a taxa de desemprego de alguns estados,
mostrar a média, quantos estados estão acima de 10% e classificar cada um.

Saída esperada:
    Média: 10.12
    Estados acima de 10%: 3
    BA: ALTO
    SP: MÉDIO
    SC: BAIXO
    PE: ALTO
    RS: BAIXO
    AM: ALTO

COMO RESOLVER:
  1. Rode:  python exercicios_corrigir/ex01_python_basico.py
  2. Leia a ÚLTIMA linha do erro (tipo do erro) e o número da linha.
  3. Corrija UM erro, rode de novo. Repita.
  4. Quando não der mais erro, CONFIRA se a saída bate com a esperada
     (erros de LÓGICA não mostram mensagem!).
Gabarito: exercicios_corrigir/gabarito/ex01_python_basico.py
"""

estados = ["BA", "SP", "SC", "PE", "RS", "AM"]
taxas = [14.0, 8.5, 4.2, 13.8, 5.1, 15.1]

def media(valores)
    total = 0
    for v in valores:
        total = total + v
    resultado = total / len(valores)

def classificar(taxa):
    if taxa >= 12:
        return "ALTO"
    elif taxa >= 8:
        return "MÉDIO"
    else
        return "BAIXO"

print("Média: " + round(media(taxas), 2))

acima = 0
for t in taxas:
    if t = 10:
        acima = acima + 1
print("Estados acima de 10%:", acima)

for i in range(len(estados) - 1):
print(f"{estados[i]}: {classificar(taxas[i])}")
