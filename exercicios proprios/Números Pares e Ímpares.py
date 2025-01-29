# 📝 Atividade: Contagem de Números Pares e Ímpares
# Crie um programa que permita ao usuário digitar 10 números e, ao final, exiba:
# ✅ A quantidade de números pares
# ✅ A quantidade de números ímpares

# Regras:
# O programa deve pedir 10 números ao usuário.
# Armazene os números em uma lista.
# # Use um loop for para contar quantos são pares e quantos são ímpares sem usar count().

# 💡 Dicas:
# ✔ Um número é par se num % 2 == 0.
# ✔ Caso contrário, ele é ímpar.
# ✔ Use duas variáveis (pares e impares) para contar dentro do for.

# Se quiser, posso te ajudar com a estrutura do código! 🚀

lista = []
par = [0]
impar = [0]

for i in range(10):
    num = int(input(f"Digite o {i+1}° número: "))
    lista.append(num)

