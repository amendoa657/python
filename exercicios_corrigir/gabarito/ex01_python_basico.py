"""
GABARITO 01 — Python básico (7 erros)

 #  Linha original                       Tipo         Correção
 1  def media(valores)                   SyntaxError  faltou ":" no final do def
 2  (sem return na função media)         LÓGICA       sem return a função devolve None -> round(None) dá TypeError
 3  else                                 SyntaxError  faltou ":" depois do else
 4  "Média: " + round(...)               TypeError    não dá para somar str + float -> usar f-string ou str()
 5  if t = 10:                           SyntaxError  "=" é atribuição; comparação é ">" (enunciado: ACIMA de 10)
 6  range(len(estados) - 1)              LÓGICA       o "-1" pula o último estado (AM). range(len(x)) já vai de 0 a n-1
 7  print sem indentação dentro do for   IndentationError  o corpo do for precisa de 4 espaços
"""

estados = ["BA", "SP", "SC", "PE", "RS", "AM"]
taxas = [14.0, 8.5, 4.2, 13.8, 5.1, 15.1]

def media(valores):                       # CORRIGIDO (1): ":" no final
    total = 0
    for v in valores:
        total = total + v
    resultado = total / len(valores)
    return resultado                      # CORRIGIDO (2): devolver o resultado

def classificar(taxa):
    if taxa >= 12:
        return "ALTO"
    elif taxa >= 8:
        return "MÉDIO"
    else:                                 # CORRIGIDO (3): ":" no else
        return "BAIXO"

print(f"Média: {media(taxas):.2f}")       # CORRIGIDO (4): f-string (ou "Média: " + str(round(...,2)))

acima = 0
for t in taxas:
    if t > 10:                            # CORRIGIDO (5): comparação ">" e não atribuição "="
        acima = acima + 1
print("Estados acima de 10%:", acima)

for i in range(len(estados)):             # CORRIGIDO (6): sem o -1
    print(f"{estados[i]}: {classificar(taxas[i])}")   # CORRIGIDO (7): indentado

# Jeito mais "pythônico" de percorrer duas listas juntas:
#   for uf, t in zip(estados, taxas):
#       print(f"{uf}: {classificar(t)}")
