# 📝 Atividade: Descobrindo o Maior e o Menor Número
# Crie um programa que permita ao usuário digitar 5 números e, ao final, exiba:
# ✅ O maior número digitado
# ✅ O menor número digitado

# Regras:
# O programa deve pedir 5 números ao usuário.
# Armazene os números em uma lista.
# Use um loop para encontrar o maior e o menor número sem usar max() ou min().

numeros = []

for i in range(5):
    num = int(input(f"digite {i+1}º numero: "))
    numeros.append(num)

print(numeros)

maior =  numeros[0]
menor = numeros[0]

for num in numeros:
    if num > maior:
        maior = num
    if num < menor:
        menor = num

print(f"O maior número é: {maior}")
print(f"O menor número é: {menor}")
