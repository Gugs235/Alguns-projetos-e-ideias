# 📝 Atividade: Média, Maior e Menor Número
# Crie um programa que permita ao usuário digitar 5 números e, ao final, exiba:
# ✅ O maior número digitado
# ✅ O menor número digitado
# ✅ A média dos números

# Regras:
# O programa deve pedir 5 números ao usuário.
# Armazene os números em uma lista.
# Use um loop for para encontrar o maior, o menor e calcular a média sem usar max(), min() ou sum().


numeros = []
for i in range(5):
    num = int(input(f"Digite o {i+1}º número: "))
    numeros.append(num)

maior = numeros[0]
menor = numeros[0]

for num in numeros:
    if num > maior:
        maior = num
    if num < menor:
        menor = num



print(f"O maior número é: {maior}")
print(f"O menor número é: {menor}")
print(f"A média é: {media}")