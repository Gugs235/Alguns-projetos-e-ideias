import sqlite3

# Adiciona cores ao terminal (se suportado)
RED = "\033[91m"   # Vermelho para assentos ocupados
GREEN = "\033[92m" # Verde para assentos livres
RESET = "\033[0m"  # Resetar cor padrão

def exibir_dados():
    conexao = sqlite3.connect("cinema.db")
    cursor = conexao.cursor()

    print("\n🔹 Cinemas Disponíveis:")
    cursor.execute("SELECT * FROM cinemas")
    cinemas = cursor.fetchall()
    for cinema in cinemas:
        print(f"ID: {cinema[0]} - Nome: {cinema[1]}")

    print("\n🎬 Filmes Disponíveis:")
    cursor.execute("SELECT * FROM filmes")
    filmes = cursor.fetchall()
    for filme in filmes:
        print(f"ID: {filme[0]} - Cinema ID: {filme[1]} - Nome: {filme[2]}")

    print("\n🎟️ Assentos Disponíveis:")
    cursor.execute("SELECT * FROM assentos")
    assentos = cursor.fetchall()
    for assento in assentos:
        status = f"{RED}Ocupado{RESET}" if assento[3] == 1 else f"{GREEN}Livre{RESET}"
        print(f"ID: {assento[0]} - Filme ID: {assento[1]} - Assento: {assento[2]} - Status: {status}")

    conexao.close()

if __name__ == "__main__":
    exibir_dados()
