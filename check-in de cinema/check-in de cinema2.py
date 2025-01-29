# check in de cinema 2.0

import sys

# Dados iniciais do sistema
cinemas = {
    "Cinema 1": {"filmes": ["Filme A", "Filme B"], "assentos": [["O"] * 10 for _ in range(5)]},
    "Cinema 2": {"filmes": ["Filme C", "Filme D"], "assentos": [["O"] * 10 for _ in range(5)]},
    "Cinema 3": {"filmes": ["Filme E", "Filme F"], "assentos": [["O"] * 10 for _ in range(5)]},
}

horarios = ["14:00", "17:00", "20:00", "23:00"]
formas_pagamento = ["Cartão de Crédito", "Cartão de Débito", "Pix", "Boleto"]

# Funções auxiliares
def mostrar_assentos(assentos):
    print("Assentos: (O = Livre, X = Ocupado)")
    for i, linha in enumerate(assentos):
        print(f"Linha {i + 1}: {' '.join(linha)}")
    print()

def escolher_assento(assentos):
    while True:
        mostrar_assentos(assentos)
        linha = int(input("Escolha a linha (1-5): ")) - 1
        coluna = int(input("Escolha a coluna (1-10): ")) - 1

        if assentos[linha][coluna] == "O":
            assentos[linha][coluna] = "X"
            print("Assento reservado com sucesso!")
            return
        else:
            print("Assento já ocupado. Escolha outro.")

def selecionar_opcao(lista, mensagem):
    for i, item in enumerate(lista, start=1):
        print(f"{i}. {item}")
    escolha = int(input(mensagem)) - 1
    return lista[escolha]

# Fluxo principal
def main():
    print("Bem-vindo ao sistema de check-in de cinema!\n")

    # Escolha do cinema
    cinema = selecionar_opcao(list(cinemas.keys()), "Escolha o cinema: ")

    # Escolha do filme
    filmes = cinemas[cinema]["filmes"]
    filme = selecionar_opcao(filmes, "Escolha o filme: ")

    # Escolha do dia e horário
    dia = input("Digite o dia desejado (DD/MM/AAAA): ")
    horario = selecionar_opcao(horarios, "Escolha o horário: ")

    # Escolha do assento
    print(f"\nEscolha o(s) assento(s) para o filme '{filme}' no {cinema}.")
    while True:
        escolher_assento(cinemas[cinema]["assentos"])
        continuar = input("Deseja escolher outro assento? (s/n): ").lower()
        if continuar != "s":
            break

    # Escolha da forma de pagamento
    print("\nEscolha a forma de pagamento:")
    forma_pagamento = selecionar_opcao(formas_pagamento, "Digite a opção: ")

    # Pagamento e resumo
    preco = 20.00  # Preço fixo por ingresso
    print("\nResumo da compra:")
    print(f"Cinema: {cinema}")
    print(f"Filme: {filme}")
    print(f"Dia: {dia}")
    print(f"Horário: {horario}")
    print(f"Forma de pagamento: {forma_pagamento}")
    total = sum(linha.count("X") for linha in cinemas[cinema]["assentos"]) * preco
    print(f"Total: R$ {total:.2f}")

    print("\nObrigado pela sua compra! Aproveite o filme!")

# Executar o programa
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nOperação cancelada.")
        sys.exit(0)
