# database.py
import sqlite3
import os

def init_db():
    db_path = 'cinema.db'
    if os.path.exists(db_path):
        os.remove(db_path)
        print("Banco de dados antigo removido.")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Tabela de Usuários
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            sobrenome TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            senha TEXT NOT NULL
        )
    ''')

    # Tabela de Cartões (para dados sensíveis)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cartoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER,
            nome_cartao TEXT,
            numero_cartao TEXT,
            data_expiracao TEXT,
            cvv TEXT,
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
        )
    ''')

    # Tabela de Cinemas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cinemas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL
        )
    ''')

    # Tabela de Filmes (com informações adicionais)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS filmes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            cinema_id INTEGER,
            duracao TEXT,
            data_lancamento TEXT,
            genero TEXT,
            classificacao TEXT,
            sinopse TEXT,
            trailer_url TEXT,
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
            tipo_sala TEXT NOT NULL,
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

    # Tabela de Reservas (Compras)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reservas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER,
            sessao_id INTEGER,
            assento_id INTEGER,
            forma_pagamento TEXT NOT NULL,
            valor_total REAL NOT NULL,
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
            FOREIGN KEY (sessao_id) REFERENCES sessoes(id),
            FOREIGN KEY (assento_id) REFERENCES assentos(id)
        )
    ''')

    # Tabela de Favoritos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS favoritos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER,
            filme_id INTEGER,
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
            FOREIGN KEY (filme_id) REFERENCES filmes(id)
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

    # Inserir Filmes (com informações adicionais)
    filmes = [
        ("Fé para o Impossível", 1, "1h 40min", "2023-08-15", "Drama", "12", 
        "Um jovem enfrenta desafios para alcançar um milagre.", "https://www.youtube.com/watch?v=b7vP1opVt5A"),
        ("Meu Malvado Favorito 1", 1, "1h 35min", "2010-07-09", "Animação", "Livre", 
        "Gru, um vilão, adota três meninas e descobre o amor.", "https://www.youtube.com/watch?v=sUkZFetWYY0"),
        ("Meu Malvado Favorito 2", 1, "1h 38min", "2013-07-03", "Animação", "Livre", 
        "Gru é recrutado para salvar o mundo.", "https://www.youtube.com/watch?v=C0BMxGUnxA"),
        ("Meu Malvado Favorito 3", 2, "1h 36min", "2017-06-29", "Animação", "Livre", 
        "Gru conhece seu irmão gêmeo Dru.", "https://www.youtube.com/watch?v=e5e5kFPg2kA"),
        ("Meu Malvado Favorito 4", 2, "1h 40min", "2024-07-03", "Animação", "Livre", 
        "Gru enfrenta um novo vilão com sua família.", "https://www.youtube.com/watch?v=qQlr9-rXrCg"),
        ("Minions 1", 3, "1h 31min", "2015-07-09", "Animação", "Livre", 
        "Os Minions buscam um novo mestre do mal.", "https://www.youtube.com/watch?v=eisKxhjBnZ0"),
        ("Minions 2", 3, "1h 27min", "2022-07-01", "Animação", "Livre", 
        "Os Minions ajudam Gru a se tornar um vilão.", "https://www.youtube.com/watch?v=6DxjJzmYsXo"),
        ("Shrek - 2001", 1, "1h 30min", "2001-05-18", "Animação", "Livre", 
        "Shrek, um ogro, tenta resgatar uma princesa.", "https://www.youtube.com/watch?v=CwXOrW2rjWY"),
        ("Shrek 2 - 2004", 1, "1h 33min", "2004-05-19", "Animação", "Livre", 
        "Shrek conhece os pais de Fiona.", "https://www.youtube.com/watch?v=5Z0h0s2WJaQ"),
        ("Shrek Terceiro - 2007", 2, "1h 33min", "2007-05-18", "Animação", "Livre", 
        "Shrek precisa encontrar um novo rei para o trono.", "https://www.youtube.com/watch?v=PhS7XAv1t1k"),
        ("Shrek no Natal", 2, "30min", "2007-11-28", "Animação", "Livre", 
        "Shrek tenta celebrar o Natal pela primeira vez.", "https://www.youtube.com/watch?v=9xS9gM1gms0"),
        ("Shrek para Sempre - 2010", 3, "1h 33min", "2010-05-21", "Animação", "Livre", 
        "Shrek faz um pacto que muda sua realidade.", "https://www.youtube.com/watch?v=SLMiCGl4Sfs"),
        ("O Susto de Shrek - 2010", 3, "30min", "2010-10-28", "Animação", "Livre", 
        "Shrek organiza uma competição de sustos no Halloween.", "https://www.youtube.com/watch?v=9xS9gM1gms0"),  # Usando o mesmo trailer de "Shrek no Natal" como placeholder
        ("Shrek 5 - 2026", 1, "1h 35min", "2026-05-20", "Animação", "Livre", 
        "Shrek retorna para uma nova aventura.", "https://www.youtube.com/watch?v=CwXOrW2rjWY"),  # Placeholder
        ("Capitão América: Admirável Mundo Novo", 2, "2h 10min", "2025-02-14", "Ação", "14", 
        "Sam Wilson enfrenta novas ameaças como Capitão América.", "https://www.youtube.com/watch?v=O_A8HdCDaWM"),
        ("Sonic 1", 3, "1h 39min", "2020-02-14", "Aventura", "Livre", 
        "Sonic se junta a um amigo humano para deter o Dr. Robotnik.", "https://www.youtube.com/watch?v=szby7ZHLnkA"),
        ("Sonic 2", 1, "2h 02min", "2022-04-08", "Aventura", "Livre", 
        "Sonic enfrenta Knuckles e o Dr. Robotnik.", "https://www.youtube.com/watch?v=47r8FXYZWNU"),
        ("Sonic 3", 2, "2h 05min", "2024-12-20", "Aventura", "Livre", 
        "Sonic e amigos lutam contra Shadow.", "https://www.youtube.com/watch?v=qSu6iXzF4oc"),
        ("Vingadores Ultimato", 3, "3h 01min", "2019-04-26", "Ação", "12", 
        "Os Vingadores tentam reverter o estalo de Thanos.", "https://www.youtube.com/watch?v=TcMBFSGVi1c"),
        ("Wicked", 1, "2h 30min", "2024-11-27", "Musical", "10", 
        "A história de Elphaba e Glinda antes de O Mágico de Oz.", "https://www.youtube.com/watch?v=F1dvwe-d0uE"),
        ("Fragmentados", 2, "1h 52min", "2016-09-22", "Suspense", "16", 
        "Três personalidades de um homem sequestram uma jovem.", "https://www.youtube.com/watch?v=84TouqfIsiI"),
        ("Telefone Preto", 3, "1h 43min", "2022-06-24", "Terror", "16", 
        "Uma criança sequestrada recebe ajuda de vítimas do passado.", "https://www.youtube.com/watch?v=A1DmL8tDaoA"),
        ("Invocação do Mal", 1, "1h 52min", "2013-07-19", "Terror", "16", 
        "Investigadores paranormais enfrentam uma entidade demoníaca.", "https://www.youtube.com/watch?v=k10ETZ41q5o"),
    ]
    for filme, cinema_id, duracao, data_lancamento, genero, classificacao, sinopse, trailer_url in filmes:
        cursor.execute("INSERT INTO filmes (nome, cinema_id, duracao, data_lancamento, genero, classificacao, sinopse, trailer_url) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", 
                       (filme, cinema_id, duracao, data_lancamento, genero, classificacao, sinopse, trailer_url))

    # Inserir Sessões (Dias, Horários e Tipos de Sala)
    sessoes = [
        (1, "2025-03-15", "14:00", "Convencional", 50),
        (1, "2025-03-15", "18:00", "IMAX", 50),
        (2, "2025-03-15", "15:00", "3D", 50),
        (3, "2025-03-16", "16:00", "VIP", 30),
        (4, "2025-03-15", "14:30", "Drive-in", 20),
        (5, "2025-03-16", "17:00", "Convencional", 50),
        (6, "2025-03-15", "13:00", "IMAX", 50),
        (7, "2025-03-16", "19:00", "3D", 50),
        (8, "2025-03-15", "16:00", "VIP", 30),
        (9, "2025-03-16", "14:00", "Drive-in", 20),
        (10, "2025-03-15", "18:30", "Convencional", 50),
        (11, "2025-03-15", "20:00", "IMAX", 50),
        (12, "2025-03-16", "15:00", "3D", 50),
        (13, "2025-03-16", "17:30", "VIP", 30),
        (14, "2025-03-15", "19:00", "Drive-in", 20),
        (15, "2025-03-15", "21:00", "Convencional", 50),
        (16, "2025-03-16", "14:00", "IMAX", 50),
        (17, "2025-03-15", "16:30", "3D", 50),
        (18, "2025-03-16", "18:00", "VIP", 30),
        (19, "2025-03-15", "20:30", "Drive-in", 20),
        (20, "2025-03-16", "13:30", "Convencional", 50),
        (21, "2025-03-15", "15:30", "IMAX", 50),
        (22, "2025-03-16", "16:00", "3D", 50),
        (23, "2025-03-15", "19:30", "VIP", 30)
    ]
    for filme_id, data, horario, tipo_sala, lotacao in sessoes:
        cursor.execute("INSERT INTO sessoes (filme_id, data, horario, tipo_sala, lotacao_maxima) VALUES (?, ?, ?, ?, ?)", 
                       (filme_id, data, horario, tipo_sala, lotacao))

    # Criar assentos para cada sessão
    cursor.execute("SELECT id FROM sessoes")
    sessoes_ids = [row[0] for row in cursor.fetchall()]
    for sessao_id in sessoes_ids:
        for i in range(1, 51):
            cursor.execute("INSERT OR IGNORE INTO assentos (sessao_id, numero) VALUES (?, ?)", 
                           (sessao_id, f"A{i}"))

    conn.commit()
    conn.close()
    print("Banco de dados inicializado com sucesso.")

if __name__ == "__main__":
    init_db()