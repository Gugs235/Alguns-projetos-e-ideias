import sqlite3
import sys

# Adiciona cores ao terminal (se suportado)
RED = "\033[91m"   # Vermelho para assentos ocupados
GREEN = "\033[92m" # Verde para assentos livres
RESET = "\033[0m"  # Resetar cor padrão

# Cria uma conexão com o banco de dados
conexao = sqlite3.connect('cinema.db')
cursor = conexao.cursor()

# Cria tabelas se não existirem
cursor.execute('''
    CREATE TABLE IF NOT EXISTS cinemas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS filmes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cinema_id INTEGER,
        nome TEXT,
        FOREIGN KEY (cinema_id) REFERENCES cinemas(id)
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS assentos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        filme_id INTEGER,
        assento TEXT UNIQUE,
        ocupado INTEGER DEFAULT 0,
        FOREIGN KEY (filme_id) REFERENCES filmes(id)
    )
''')
conexao.commit()

# Função para verificar se o assento está ocupado
def verificar_assento(assento):
    cursor.execute("SELECT ocupado FROM assentos WHERE assento = ?", (assento,))
    resultado = cursor.fetchone()
    if resultado is None:
        return f"{RED}Assento {assento} não encontrado!{RESET}"
    return f"{RED}Assento {assento} ocupado!{RESET}" if resultado[0] == 1 else f"{GREEN}Assento {assento} livre!{RESET}"

# Função para reservar assento
def reservar_assento(assento):
    cursor.execute("SELECT ocupado FROM assentos WHERE assento = ?", (assento,))
    resultado = cursor.fetchone()
    if resultado is None:
        return f"{RED}Assento {assento} não encontrado!{RESET}"
    if resultado[0] == 0:
        cursor.execute("UPDATE assentos SET ocupado = 1 WHERE assento = ?", (assento,))
        conexao.commit()
        return f"{GREEN}Assento {assento} reservado com sucesso!{RESET}"
    return f"{RED}Assento {assento} já está ocupado!{RESET}"

# Função para liberar assento
def liberar_assento(assento):
    cursor.execute("SELECT ocupado FROM assentos WHERE assento = ?", (assento,))
    resultado = cursor.fetchone()
    if resultado is None:
        return f"{RED}Assento {assento} não encontrado!{RESET}"
    if resultado[0] == 1:
        cursor.execute("UPDATE assentos SET ocupado = 0 WHERE assento = ?", (assento,))
        conexao.commit()
        return f"{GREEN}Assento {assento} liberado com sucesso!{RESET}"
    return f"{RED}Assento {assento} já está livre!{RESET}"

# Função para exibir todos os assentos
def exibir_assentos():
    cursor.execute("SELECT assento, ocupado FROM assentos")
    resultado = cursor.fetchall()
    if not resultado:
        print("Nenhum assento cadastrado.")
        return
    for assento in resultado:
        status = f"{RED}Ocupado{RESET}" if assento[1] == 1 else f"{GREEN}Livre{RESET}"
        print(f"Assento {assento[0]} - {status}")

# Função para exibir dados do cinema
def exibir_dados():
    print("\n🔹 Cinemas Disponíveis:")
    cursor.execute("SELECT * FROM cinemas")
    cinemas = cursor.fetchall()
    if cinemas:
        for cinema in cinemas:
            print(f"ID: {cinema[0]} - Nome: {cinema[1]}")
    else:
        print("Nenhum cinema cadastrado.")

    print("\n🎬 Filmes Disponíveis:")
    cursor.execute("SELECT * FROM filmes")
    filmes = cursor.fetchall()
    if filmes:
        for filme in filmes:
            print(f"ID: {filme[0]} - Cinema ID: {filme[1]} - Nome: {filme[2]}")
    else:
        print("Nenhum filme cadastrado.")

    print("\n🎟️ Assentos Disponíveis:")
    cursor.execute("SELECT assento, ocupado FROM assentos")
    assentos = cursor.fetchall()
    if assentos:
        for assento in assentos:
            status = f"{RED}Ocupado{RESET}" if assento[1] == 1 else f"{GREEN}Livre{RESET}"
            print(f"Assento: {assento[0]} - Status: {status}")
    else:
        print("Nenhum assento cadastrado.")

# Função para criar um cinema
def criar_cinema():
    nome = input("Digite o nome do cinema: ")
    cursor.execute("INSERT INTO cinemas (nome) VALUES (?)", (nome,))
    conexao.commit()
    print(f"Cinema '{nome}' criado com sucesso!")

# Função para criar um filme
def criar_filme():
    cinema_id = input("Digite o ID do cinema: ")
    nome = input("Digite o nome do filme: ")
    cursor.execute("INSERT INTO filmes (cinema_id, nome) VALUES (?, ?)", (cinema_id, nome))
    conexao.commit()
    print(f"Filme '{nome}' criado com sucesso!")

# Função para criar um assento
def criar_assento():
    filme_id = input("Digite o ID do filme: ")
    assento = input("Digite o assento: ")
    cursor.execute("INSERT INTO assentos (filme_id, assento, ocupado) VALUES (?, ?, 0)", (filme_id, assento))
    conexao.commit()
    print(f"Assento '{assento}' criado com sucesso!")

# Função para liberar um assento específico
def liberar_assentos():
    assento = input("Digite o assento que deseja liberar: ")
    print(liberar_assento(assento))

# Menu principal
if __name__ == "__main__":
    while True:
        print("\n🎬 Menu -------------------------")
        print("1. Listar cinemas")
        print("2. Listar filmes")
        print("3. Listar assentos")
        print("4. Criar cinema")
        print("5. Criar filme")
        print("6. Criar assento")
        print("7. Reservar assento")
        print("8. Liberar assento")
        print("9. Sair")
        
        opcao = input("Digite a opção desejada: ")
        
        if opcao == "1":
            exibir_dados()
        elif opcao == "2":
            exibir_dados()
        elif opcao == "3":
            exibir_assentos()
        elif opcao == "4":
            criar_cinema()
        elif opcao == "5":
            criar_filme()
        elif opcao == "6":
            criar_assento()
        elif opcao == "7":
            assento = input("Digite o assento que deseja reservar: ")
            print(reservar_assento(assento))
        elif opcao == "8":
            liberar_assentos()
        elif opcao == "9":
            print("Obrigado por usar o sistema de assentos!")
            break
        else:
            print("Opção inválida. Por favor, tente novamente.")
