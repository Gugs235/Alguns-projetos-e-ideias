# database.py
import mysql.connector
from mysql.connector import Error

class CinemaDatabase:
    def __init__(self):
        self.conn = None
        self.cursor = None
        self.conectar()

    def conectar(self):
        try:
            self.conn = mysql.connector.connect(
                host='localhost',
                database='Checkin_Cinema',
                user='suporte',
                password='suporte'
            )
            if self.conn.is_connected():
                self.cursor = self.conn.cursor()
                print("Conectado ao MySQL com sucesso!")
                self.criar_tabelas()
                self.inserir_dados_iniciais()
        except Error as e:
            print(f"Erro ao conectar ao MySQL: {e}")

    def criar_tabelas(self):
        tabelas = [
            """
            CREATE TABLE IF NOT EXISTS usuarios (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nome VARCHAR(255) NOT NULL,
                sobrenome VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL UNIQUE,
                senha VARCHAR(255) NOT NULL
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS cartoes (
                id INT AUTO_INCREMENT PRIMARY KEY,
                usuario_id INT,
                nome_cartao VARCHAR(255) NOT NULL,
                numero_cartao VARCHAR(16) NOT NULL,
                data_expiracao VARCHAR(5) NOT NULL,
                cvv VARCHAR(3) NOT NULL,
                FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS cinemas (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nome VARCHAR(255) NOT NULL
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS filmes (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nome VARCHAR(255) NOT NULL,
                cinema_id INT,
                duracao TIME NOT NULL,
                data_lancamento DATE NOT NULL,
                genero VARCHAR(255) NOT NULL,
                classificacao VARCHAR(255) NOT NULL,
                sinopse TEXT NOT NULL,
                trailer_url VARCHAR(255) NOT NULL,
                poster_path VARCHAR(255),  -- Novo campo para o caminho do pôster
                FOREIGN KEY (cinema_id) REFERENCES cinemas(id)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS sessoes (
                id INT AUTO_INCREMENT PRIMARY KEY,
                filme_id INT NOT NULL,
                cinema_id INT NOT NULL,
                data DATE NOT NULL,
                horario TIME NOT NULL,
                tipo_sala VARCHAR(255) NOT NULL,
                lotacao_maxima INT NOT NULL,
                FOREIGN KEY (filme_id) REFERENCES filmes(id),
                FOREIGN KEY (cinema_id) REFERENCES cinemas(id)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS filmes (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nome VARCHAR(255) NOT NULL,
                cinema_id INT,
                duracao TIME NOT NULL,
                data_lancamento DATE NOT NULL,
                genero VARCHAR(255) NOT NULL,
                classificacao VARCHAR(255) NOT NULL,
                sinopse TEXT NOT NULL,
                trailer_url VARCHAR(255) NOT NULL,
                poster_data MEDIUMBLOB,  -- Novo campo para armazenar os dados binários da imagem
                FOREIGN KEY (cinema_id) REFERENCES cinemas(id)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS assentos (
                id INT AUTO_INCREMENT PRIMARY KEY,
                sessao_id INT,
                numero VARCHAR(255) NOT NULL,
                reservado BOOLEAN NOT NULL DEFAULT FALSE,
                FOREIGN KEY (sessao_id) REFERENCES sessoes(id)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS reservas (
                id INT AUTO_INCREMENT PRIMARY KEY,
                usuario_id INT,
                sessao_id INT,
                assento_id INT,
                forma_pagamento VARCHAR(255) NOT NULL,
                valor_total DECIMAL(10, 2) NOT NULL,
                FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
                FOREIGN KEY (sessao_id) REFERENCES sessoes(id),
                FOREIGN KEY (assento_id) REFERENCES assentos(id)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS favoritos (
                id INT AUTO_INCREMENT PRIMARY KEY,
                usuario_id INT NOT NULL,
                filme_id INT NOT NULL,
                FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
                FOREIGN KEY (filme_id) REFERENCES filmes(id)
            )
            """
        ]
        for tabela in tabelas:
            self.cursor.execute(tabela)
            self.conn.commit()

            # Verificar a estrutura da tabela filmes
            self.cursor.execute("SHOW COLUMNS FROM filmes")
            colunas = [coluna[0] for coluna in self.cursor.fetchall()]
            colunas_esperadas = ['id', 'nome', 'cinema_id', 'duracao', 'data_lancamento', 'genero', 'classificacao', 'sinopse', 'trailer_url', 'poster_data']
            for coluna in colunas_esperadas:
                if coluna not in colunas:
                    if coluna == 'poster_data':
                        self.cursor.execute("ALTER TABLE filmes ADD COLUMN poster_data MEDIUMBLOB")
                        self.conn.commit()
                        print("Coluna 'poster_data' adicionada à tabela 'filmes'.")
                    else:
                        raise Exception(f"Coluna '{coluna}' não encontrada na tabela 'filmes'. Estrutura do banco de dados está incorreta.")
            print("Estrutura da tabela 'filmes' verificada com sucesso.")

        # Verificar a estrutura da tabela sessoes
        self.cursor.execute("SHOW COLUMNS FROM sessoes")
        colunas_sessoes = [coluna[0] for coluna in self.cursor.fetchall()]
        colunas_esperadas_sessoes = ['id', 'filme_id', 'cinema_id', 'data', 'horario', 'tipo_sala', 'lotacao_maxima']
        for coluna in colunas_esperadas_sessoes:
            if coluna not in colunas_sessoes:
                # Desativar verificações de chave estrangeira
                self.cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
                # Dropar tabelas dependentes antes de recriar a tabela sessoes
                self.cursor.execute("DROP TABLE IF EXISTS reservas")
                self.cursor.execute("DROP TABLE IF EXISTS assentos")
                self.cursor.execute("DROP TABLE IF EXISTS sessoes")
                self.cursor.execute("""
                    CREATE TABLE sessoes (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        filme_id INT NOT NULL,
                        cinema_id INT NOT NULL,
                        data DATE NOT NULL,
                        horario TIME NOT NULL,
                        tipo_sala VARCHAR(255) NOT NULL,
                        lotacao_maxima INT NOT NULL,
                        FOREIGN KEY (filme_id) REFERENCES filmes(id),
                        FOREIGN KEY (cinema_id) REFERENCES cinemas(id)
                    )
                """)
                # Recriar tabelas dependentes
                self.cursor.execute("""
                    CREATE TABLE IF NOT EXISTS assentos (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        sessao_id INT,
                        numero VARCHAR(255) NOT NULL,
                        reservado BOOLEAN NOT NULL DEFAULT FALSE,
                        FOREIGN KEY (sessao_id) REFERENCES sessoes(id)
                    )
                """)
                self.cursor.execute("""
                    CREATE TABLE IF NOT EXISTS reservas (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        usuario_id INT,
                        sessao_id INT,
                        assento_id INT,
                        forma_pagamento VARCHAR(255) NOT NULL,
                        valor_total DECIMAL(10, 2) NOT NULL,
                        FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
                        FOREIGN KEY (sessao_id) REFERENCES sessoes(id),
                        FOREIGN KEY (assento_id) REFERENCES assentos(id)
                    )
                """)
                # Reativar verificações de chave estrangeira
                self.cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
                self.conn.commit()
                print(f"Tabela 'sessoes' e tabelas dependentes recriadas com a coluna '{coluna}'.")
                break
        print("Estrutura da tabela 'sessoes' verificada com sucesso.")

        # Verificar a estrutura da tabela favoritos
        self.cursor.execute("SHOW COLUMNS FROM favoritos")
        colunas_favoritos = [coluna[0] for coluna in self.cursor.fetchall()]
        colunas_esperadas_favoritos = ['id', 'usuario_id', 'filme_id']
        for coluna in colunas_esperadas_favoritos:
            if coluna not in colunas_favoritos:
                # Desativar verificações de chave estrangeira
                self.cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
                # Dropar a tabela favoritos e recriá-la
                self.cursor.execute("DROP TABLE IF EXISTS favoritos")
                self.cursor.execute("""
                    CREATE TABLE favoritos (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        usuario_id INT NOT NULL,
                        filme_id INT NOT NULL,
                        FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
                        FOREIGN KEY (filme_id) REFERENCES filmes(id)
                    )
                """)
                # Reativar verificações de chave estrangeira
                self.cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
                self.conn.commit()
                print(f"Tabela 'favoritos' recriada com a coluna '{coluna}'.")
                break
        print("Estrutura da tabela 'favoritos' verificada com sucesso.")

    def inserir_dados_iniciais(self):
        import requests  # Adicionar import para baixar imagens
        # Verificar se já existem dados na tabela cinemas
        self.cursor.execute("SELECT COUNT(*) FROM cinemas")
        count = self.cursor.fetchone()[0]
        print(f"Total de cinemas no banco: {count}")

        if count == 0:  # Só insere se a tabela estiver vazia
            print("Inserindo dados iniciais...")
            # Cinemas
            cinemas = [
                "Cinemark - Shopping",
                "Cinépolis Norte Sul Plaza",
                "UCI Bosque Dos Ipês"
            ]
            for cinema in cinemas:
                self.cursor.execute("INSERT INTO cinemas (nome) VALUES (%s)", (cinema,))
            self.conn.commit()
            print(f"Inseridos {len(cinemas)} cinemas.")

            # Filmes com o novo campo poster_path
# No arquivo database.py, na função inserir_dados_iniciais
            filmes = [
                ("Fé para o Impossível", 1, "01:40:00", "2023-08-15", "Drama", "12", 
                "Um jovem enfrenta desafios para alcançar um milagre.", "https://www.youtube.com/watch?v=b7vP1opVt5A", 
                "https://br.web.img3.acsta.net/r_1920_1080/img/68/4c/684cb2caf5f1442da5ef8d376c32ec04.jpg"),
                ("Meu Malvado Favorito 1", 1, "01:35:00", "2010-07-09", "Animação", "Livre", 
                "Gru, um vilão, adota três meninas e descobre o amor.", "https://www.youtube.com/watch?v=sUkZFetWYY0", 
                "https://br.web.img3.acsta.net/r_1920_1080/pictures/23/05/05/16/09/2641829.jpg"),
                ("Meu Malvado Favorito 2", 1, "01:38:00", "2013-07-03", "Animação", "Livre", 
                "Gru é recrutado para salvar o mundo.", "https://youtu.be/gi2QWNZ9jms?si=DbPr2-JSSfbGU4ML", 
                "https://br.web.img2.acsta.net/r_1920_1080/pictures/210/173/21017357_2013070316550589.jpg"),
                ("Meu Malvado Favorito 3", 2, "01:36:00", "2017-06-29", "Animação", "Livre", 
                "Gru conhece seu irmão gêmeo Dru.", "https://www.youtube.com/watch?v=e5e5kFPg2kA", 
                "https://br.web.img2.acsta.net/pictures/17/03/14/20/37/126690.jpg"),
                ("Meu Malvado Favorito 4", 2, "01:40:00", "2024-07-03", "Animação", "Livre", 
                "Gru enfrenta um novo vilão com sua família.", "https://www.youtube.com/watch?v=qQlr9-rXrCg", 
                "https://br.web.img3.acsta.net/r_1920_1080/img/6c/71/6c71afa89fd8ed8999b3e04d8d794a0e.jpg"),
                ("Minions 1", 3, "01:31:00", "2015-07-09", "Animação", "Livre", 
                "Os Minions buscam um novo mestre do mal.", "https://www.youtube.com/watch?v=eisKxhjBnZ0", 
                "https://br.web.img3.acsta.net/r_1920_1080/img/08/89/08892c6553a80e2e71ca85f3eb1635d8.jpg"),
                ("Minions 2", 3, "01:27:00", "2022-07-01", "Animação", "Livre", 
                "Os Minions ajudam Gru a se tornar um vilão.", "https://www.youtube.com/watch?v=6DxjJzmYsXo", 
                "https://br.web.img3.acsta.net/pictures/20/02/03/15/22/4954456.jpg"),
                ("Shrek - 2001", 1, "01:30:00", "2001-05-18", "Animação", "Livre", 
                "Shrek, um ogro, tenta resgatar uma princesa.", "https://www.youtube.com/watch?v=CwXOrW2rjWY", 
                "https://img.elo7.com.br/product/zoom/42EF263/poster-3-shrek-2001-mdf-3mm-28x40cm-ogro.jpg"),
                ("Shrek 2 - 2004", 1, "01:33:00", "2004-05-19", "Animação", "Livre", 
                "Shrek conhece os pais de Fiona.", "https://www.youtube.com/watch?v=5Z0h0s2WJaQ", 
                "https://br.web.img2.acsta.net/medias/nmedia/18/97/04/22/20504502.jpg"),
                ("Shrek Terceiro - 2007", 2, "01:33:00", "2007-05-18", "Animação", "Livre", 
                "Shrek precisa encontrar um novo rei para o trono.", "https://www.youtube.com/watch?v=PhS7XAv1t1k", 
                "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSCNpaUkUFwrG_UQEWQmjI9bBz8dt6gXphzTA&s.jpg"),
                ("Shrek no Natal", 2, "00:30:00", "2007-11-28", "Animação", "Livre", 
                "Shrek tenta celebrar o Natal pela primeira vez.", "https://www.youtube.com/watch?v=9xS9gM1gms0", 
                "https://br.web.img2.acsta.net/c_300_300/pictures/20/10/30/13/48/2427606.jpg"),
                ("Shrek para Sempre - 2010", 3, "01:33:00", "2010-05-21", "Animação", "Livre", 
                "Shrek faz um pacto que muda sua realidade.", "https://www.youtube.com/watch?v=SLMiCGl4Sfs", 
                "https://br.web.img2.acsta.net/medias/nmedia/18/87/90/45/19962744.jpg"),
                ("O Susto de Shrek - 2010", 3, "00:30:00", "2010-10-28", "Animação", "Livre", 
                "Shrek organiza uma competição de sustos no Halloween.", "https://www.youtube.com/watch?v=9xS9gM1gms0", 
                "https://m.media-amazon.com/images/M/MV5BMDg0NDUwYjItMmRjYi00MzNjLTkyY2EtM2FiMjE1NWY4ZTY0XkEyXkFqcGc@._V1_.jpg"),
                ("Shrek 5 - 2026", 1, "01:35:00", "2026-05-20", "Animação", "Livre", 
                "Shrek retorna para uma nova aventura.", "https://www.youtube.com/watch?v=CwXOrW2rjWY", 
                "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR0NhwrLk9_JsWmnj19Yuw6NKabZDTjgA44gA&s"),
                ("Capitão América: Admirável Mundo Novo", 2, "02:10:00", "2025-02-14", "Ação", "14", 
                "Sam Wilson enfrenta novas ameaças como Capitão América.", "https://www.youtube.com/watch?v=O_A8HdCDaWM", 
                "https://br.web.img2.acsta.net/img/56/0c/560c72bf877f88472877898cebe00ff0.jpg"),
                ("Sonic 1", 3, "01:39:00", "2020-02-14", "Aventura", "Livre", 
                "Sonic se junta a um amigo humano para deter o Dr. Robotnik.", "https://www.youtube.com/watch?v=szby7ZHLnkA", 
                "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTPi29CQGC_FEcoQYQwxP2oqafgjIQmP56zsw&s"),
                ("Sonic 2", 1, "02:02:00", "2022-04-08", "Aventura", "Livre", 
                "Sonic enfrenta Knuckles e o Dr. Robotnik.", "https://www.youtube.com/watch?v=47r8FXYZWNU", 
                "https://sm.ign.com/t/ign_br/screenshot/default/sth2-intl-dgtl-payoff-1-sht-bra_b76q.960.jpg"),
                ("Sonic 3", 2, "02:05:00", "2024-12-20", "Aventura", "Livre", 
                "Sonic e amigos lutam contra Shadow.", "https://www.youtube.com/watch?v=qSu6iXzF4oc", 
                "https://ingresso-a.akamaihd.net/b2b/production/uploads/articles-content/f64cf04e-7707-4f9d-9f65-34534f0f59cc.jpg"),
                ("Vingadores Ultimato", 3, "03:01:00", "2019-04-26", "Ação", "12", 
                "Os Vingadores tentam reverter o estalo de Thanos.", "https://www.youtube.com/watch?v=TcMBFSGVi1c", 
                "https://m.media-amazon.com/images/M/MV5BMTc5MDE2ODcwNV5BMl5BanBnXkFtZTgwMzI2NzQ2NzM@._V1_FMjpg_UX1000_.jpg"),
                ("Wicked", 1, "02:30:00", "2024-11-27", "Musical", "10", 
                "A história de Elphaba e Glinda antes de O Mágico de Oz.", "https://www.youtube.com/watch?v=F1dvwe-d0uE", 
                "https://a-static.mlcdn.com.br/1500x1500/poster-cartaz-wicked-posterflix/poparteskins2/pos-03834-30x45cm/e92bba484442009644de7d4742b2bad0.jpeg"),
                ("Fragmentados", 2, "01:52:00", "2016-09-22", "Suspense", "16", 
                "Três personalidades de um homem sequestram uma jovem.", "https://www.youtube.com/watch?v=84TouqfIsiI", 
                "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcStsn2EtcjMJhYV4Wvwh4jdqqonSwPQp2WRWA&s"),
                ("Telefone Preto", 3, "01:43:00", "2022-06-24", "Terror", "16", 
                "Uma criança sequestrada recebe ajuda de vítimas do passado.", "https://www.youtube.com/watch?v=A1DmL8tDaoA", 
                "https://br.web.img3.acsta.net/pictures/22/06/23/21/10/1998178.jpg"),
                ("Invocação do Mal", 1, "01:52:00", "2013-07-19", "Terror", "16", 
                "Investigadores paranormais enfrentam uma entidade demoníaca.", "https://www.youtube.com/watch?v=k10ETZ41q5o", 
                "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQPTyYBnPwo2Ni0Wj81VSngSgChiKjh44bN2Q&s"),
            ]

            for filme, cinema_id, duracao, data_lancamento, genero, classificacao, sinopse, trailer_url, poster_url in filmes:
                # Baixar a imagem da URL
                poster_data = None
                try:
                    response = requests.get(poster_url, timeout=5)
                    response.raise_for_status()
                    poster_data = response.content  # Dados binários da imagem
                except Exception as e:
                    print(f"Erro ao baixar pôster de {filme}: {str(e)}")
                    continue  # Pula este filme se o download falhar

                self.cursor.execute("""
                    INSERT INTO filmes (nome, cinema_id, duracao, data_lancamento, genero, classificacao, sinopse, trailer_url, poster_data) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (filme, cinema_id, duracao, data_lancamento, genero, classificacao, sinopse, trailer_url, poster_data))
            print(f"Inseridos {len(filmes)} filmes.")

            # Sessões
            sessoes = [
                (1, 1, "2025-03-15", "14:00:00", "Convencional", 50),
                (1, 1, "2025-03-15", "18:00:00", "IMAX", 50),
                (2, 1, "2025-03-15", "15:00:00", "3D", 50),
                (3, 1, "2025-03-16", "16:00:00", "VIP", 30),
                (4, 1, "2025-03-15", "14:30:00", "Drive-in", 20),
                (5, 2, "2025-03-16", "17:00:00", "Convencional", 50),
                (6, 2, "2025-03-15", "13:00:00", "IMAX", 50),
                (7, 2, "2025-03-16", "19:00:00", "3D", 50),
                (8, 2, "2025-03-15", "16:00:00", "VIP", 30),
                (9, 2, "2025-03-16", "14:00:00", "Drive-in", 20),
                (10, 2, "2025-03-15", "18:30:00", "Convencional", 50),
                (11, 2, "2025-03-15", "20:00:00", "IMAX", 50),
                (12, 3, "2025-03-16", "15:00:00", "3D", 50),
                (13, 3, "2025-03-16", "17:30:00", "VIP", 30),
                (14, 3, "2025-03-15", "19:00:00", "Drive-in", 20),
                (15, 3, "2025-03-15", "21:00:00", "Convencional", 50),
                (16, 3, "2025-03-16", "14:00:00", "IMAX", 50),
                (17, 3, "2025-03-15", "16:30:00", "3D", 50),
                (18, 3, "2025-03-16", "18:00:00", "VIP", 30),
                (19, 3, "2025-03-15", "20:30:00", "Drive-in", 20),
                (20, 3, "2025-03-16", "13:30:00", "Convencional", 50),
                (21, 3, "2025-03-15", "15:30:00", "IMAX", 50),
                (22, 3, "2025-03-16", "16:00:00", "3D", 50),
                (23, 3, "2025-03-15", "19:30:00", "VIP", 30)
            ]
            for filme_id, cinema_id, data, horario, tipo_sala, lotacao in sessoes:
                self.cursor.execute("INSERT INTO sessoes (filme_id, cinema_id, data, horario, tipo_sala, lotacao_maxima) VALUES (%s, %s, %s, %s, %s, %s)", 
                                (filme_id, cinema_id, data, horario, tipo_sala, lotacao))
            print(f"Inseridas {len(sessoes)} sessões.")

            # Assentos
            self.cursor.execute("SELECT id FROM sessoes")
            sessoes_ids = [row[0] for row in self.cursor.fetchall()]
            for sessao_id in sessoes_ids:
                for i in range(1, 51):
                    self.cursor.execute("INSERT INTO assentos (sessao_id, numero, reservado) VALUES (%s, %s, %s)", 
                                    (sessao_id, f"A{i}", 0))
            print(f"Inseridos assentos para {len(sessoes_ids)} sessões.")

            self.conn.commit()
            print("Dados iniciais inseridos com sucesso!")

    def fechar_conexao(self):
        if self.conn.is_connected():
            self.cursor.close()
            self.conn.close()
            print("Conexão ao MySQL fechada.")
