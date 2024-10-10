# Lê o tipo de chá
# Coloque o número qualquer (número do chá)
T = int(input())

# Lê as respostas dos 5 competidores
# Colocar 5 números separados pelo espaço. ex: 5 4 3 2 1
respostas = list(map(int, input().split()))

# Conta o número de competidores que acertaram a resposta
acertos = respostas.count(T)

# Exibe o número de acertos
print(acertos)
