# database.py
import sqlite3
import os

def init_db():
    # Remove o banco de dados existente para garantir uma recriação limpa
    db_path = 'cinema.db'
    if os.path.exists(db_path):
        os.remove(db_path)
        print("Banco de dados antigo removido.")

    # Conecta ao banco de dados (será criado um novo)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Tabela de Cinemas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cinemas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL
        )
    ''')

    # Tabela de Filmes
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS filmes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            cinema_id INTEGER,
            FOREIGN KEY (cinema_id) REFERENCES cinemas(id)
        )
    ''')

    # Tabela de Sessões
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sessoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filme_id INTEGER,
            data TEXT NOT NULL,
            horario TEXT NOT NULL,
            lotacao_maxima INTEGER NOT NULL,
            FOREIGN KEY (filme_id) REFERENCES filmes(id)
        )
    ''')

    # Tabela de Assentos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS assentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sessao_id INTEGER NOT NULL,
            numero TEXT NOT NULL,
            reservado INTEGER DEFAULT 0,
            FOREIGN KEY (sessao_id) REFERENCES sessoes(id)
        )
    ''')

    # Tabela de Reservas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reservas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sessao_id INTEGER,
            assento_id INTEGER,
            forma_pagamento TEXT NOT NULL,
            valor_total REAL NOT NULL,
            FOREIGN KEY (sessao_id) REFERENCES sessoes(id),
            FOREIGN KEY (assento_id) REFERENCES assentos(id)
        )
    ''')

    # Inserir Cinemas
    cinemas = [
        "Cinemark - Shopping",
        "Cinépolis Norte Sul Plaza",
        "UCI Bosque Dos Ipês"
    ]
    for cinema in cinemas:
        cursor.execute("INSERT INTO cinemas (nome) VALUES (?)", (cinema,))

    # Inserir Filmes
    filmes = [
        ("Fé para o Impossível", 1),  # Cinemark
        ("Meu Malvado Favorito 1", 1),
        ("Meu Malvado Favorito 2", 1),
        ("Meu Malvado Favorito 3", 2),  # Cinépolis
        ("Meu Malvado Favorito 4", 2),
        ("Minions 1", 3),  # UCI
        ("Minions 2", 3),
        ("Shrek - 2001", 1),
        ("Shrek 2 - 2004", 1),
        ("Shrek Terceiro - 2007", 2),
        ("Shrek no Natal", 2),
        ("Shrek para Sempre - 2010", 3),
        ("O Susto de Shrek - 2010", 3),
        ("Shrek 5 - 2026", 1),
        ("Capitão América: Admirável Mundo Novo", 2),
        ("Sonic 1", 3),
        ("Sonic 2", 1),
        ("Sonic 3", 2),
        ("Vingadores Ultimato", 3),
        ("Wicked", 1),
        ("Fragmentados", 2),
        ("Telefone Preto", 3),
        ("Invocação do Mal", 1)
    ]
    for filme, cinema_id in filmes:
        cursor.execute("INSERT INTO filmes (nome, cinema_id) VALUES (?, ?)", (filme, cinema_id))

    # Inserir Sessões (Dias e Horários)
    sessoes = [
        (1, "2025-03-15", "14:00", 50),  # Fé para o Impossível no Cinemark
        (1, "2025-03-15", "18:00", 50),
        (2, "2025-03-15", "15:00", 50),  # Meu Malvado Favorito 1 no Cinemark
        (3, "2025-03-16", "16:00", 50),  # Meu Malvado Favorito 2 no Cinemark
        (4, "2025-03-15", "14:30", 50),  # Meu Malvado Favorito 3 na Cinépolis
        (5, "2025-03-16", "17:00", 50),  # Meu Malvado Favorito 4 na Cinépolis
        (6, "2025-03-15", "13:00", 50),  # Minions 1 na UCI
        (7, "2025-03-16", "19:00", 50),  # Minions 2 na UCI
        (8, "2025-03-15", "16:00", 50),  # Shrek - 2001 no Cinemark
        (9, "2025-03-16", "14:00", 50),  # Shrek 2 - 2004 no Cinemark
        (10, "2025-03-15", "18:30", 50), # Shrek Terceiro na Cinépolis
        (11, "2025-03-15", "20:00", 50), # Shrek no Natal na Cinépolis
        (12, "2025-03-16", "15:00", 50), # Shrek para Sempre na UCI
        (13, "2025-03-16", "17:30", 50), # O Susto de Shrek na UCI
        (14, "2025-03-15", "19:00", 50), # Shrek 5 no Cinemark
        (15, "2025-03-15", "21:00", 50), # Capitão América na Cinépolis
        (16, "2025-03-16", "14:00", 50), # Sonic 1 na UCI
        (17, "2025-03-15", "16:30", 50), # Sonic 2 no Cinemark
        (18, "2025-03-16", "18:00", 50), # Sonic 3 na Cinépolis
        (19, "2025-03-15", "20:30", 50), # Vingadores Ultimato na UCI
        (20, "2025-03-16", "13:30", 50), # Wicked no Cinemark
        (21, "2025-03-15", "15:30", 50), # Fragmentados na Cinépolis
        (22, "2025-03-16", "16:00", 50), # Telefone Preto na UCI
        (23, "2025-03-15", "19:30", 50)  # Invocação do Mal no Cinemark
    ]
    for filme_id, data, horario, lotacao in sessoes:
        cursor.execute("INSERT INTO sessoes (filme_id, data, horario, lotacao_maxima) VALUES (?, ?, ?, ?)", 
                       (filme_id, data, horario, lotacao))

    # Criar assentos para cada sessão
    cursor.execute("SELECT id FROM sessoes")
    sessoes_ids = [row[0] for row in cursor.fetchall()]
    for sessao_id in sessoes_ids:
        for i in range(1, 51):  # 50 assentos por sessão
            cursor.execute("INSERT OR IGNORE INTO assentos (sessao_id, numero) VALUES (?, ?)", 
                           (sessao_id, f"A{i}"))

    conn.commit()
    conn.close()
    print("Banco de dados inicializado com sucesso.")

if __name__ == "__main__":
    init_db()