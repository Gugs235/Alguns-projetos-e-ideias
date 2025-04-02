# backend.py
import mysql.connector
from database import CinemaDatabase
from PySide6.QtWidgets import QMessageBox
from PySide6.QtWidgets import QApplication

class CinemaBackend:
    def __init__(self):
        self.db = CinemaDatabase()
        self.conn = self.db.conn
        self.cursor = self.conn.cursor(buffered=True)

    # Função auxiliar para garantir que usuario_id seja um inteiro
    def _ensure_scalar(self, value):
        if isinstance(value, (tuple, list)):
            return value[0]
        return value

    def login_usuario(self, email, senha):
        try:
            self.cursor.execute("SELECT id, nome FROM usuarios WHERE email = %s AND senha = %s", (email, senha))
            usuario = self.cursor.fetchone()
            return usuario  # Retorna (id, nome) ou None
        except Exception as e:
            print(f"Erro ao fazer login: {str(e)}")
            return None

    def cadastrar_usuario(self, nome, sobrenome, email, senha):
        try:
            self.cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
            if self.cursor.fetchone():
                return False, "E-mail já cadastrado!"
            self.cursor.execute("INSERT INTO usuarios (nome, sobrenome, email, senha) VALUES (%s, %s, %s, %s)", 
                               (nome, sobrenome, email, senha))
            self.conn.commit()
            return True, "Cadastro realizado com sucesso!"
        except Exception as e:
            return False, f"Erro ao cadastrar: {str(e)}"

    def login(self, nome, senha):
        try:
            self.cursor.execute("SELECT id, nome, senha FROM usuarios WHERE nome = %s", (nome,))
            usuario = self.cursor.fetchone()
            if usuario and usuario[2] == senha:
                return True, usuario[0], usuario[1]
            return False, None, "Nome ou senha incorretos!"
        except Exception as e:
            return False, None, f"Erro ao fazer login: {str(e)}"

    def get_usuario_info(self, usuario_id):
        usuario_id = self._ensure_scalar(usuario_id)
        self.cursor.execute("SELECT nome, sobrenome, email, senha FROM usuarios WHERE id = %s", (usuario_id,))
        return self.cursor.fetchone()

    def get_cartao_info(self, usuario_id):
            usuario_id = self._ensure_scalar(usuario_id)
            self.cursor.execute("SELECT nome_cartao, numero_cartao, data_expiracao, cvv FROM cartoes WHERE usuario_id = %s", (usuario_id,))
            return self.cursor.fetchone()

    def salvar_cartao(self, usuario_id, nome_cartao, numero_cartao, data_expiracao, cvv):
        usuario_id = self._ensure_scalar(usuario_id)
        self.cursor.execute("""
            INSERT INTO cartoes (usuario_id, nome_cartao, numero_cartao, data_expiracao, cvv) 
            VALUES (%s, %s, %s, %s, %s) 
            ON DUPLICATE KEY UPDATE 
                nome_cartao=%s, numero_cartao=%s, data_expiracao=%s, cvv=%s
        """, (usuario_id, nome_cartao, numero_cartao, data_expiracao, cvv, nome_cartao, numero_cartao, data_expiracao, cvv))
        self.conn.commit()

    def get_filmes_all(self):
        self.cursor.execute("SELECT id, nome, cinema_id, duracao, data_lancamento, genero, classificacao, sinopse, trailer_url, poster_data FROM filmes")
        filmes = self.cursor.fetchall()
        print(f"Filmes encontrados no banco: {len(filmes)}")
        return filmes

    def get_filme_info(self, filme_id):
        self.cursor.execute("SELECT id, nome, cinema_id, duracao, data_lancamento, genero, classificacao, sinopse, trailer_url, poster_data FROM filmes WHERE id = %s", (filme_id,))
        return self.cursor.fetchone()

    def get_sessoes_info(self, filme_id):
        self.cursor.execute('''
            SELECT s.id, s.data, s.horario, s.tipo_sala, c.nome 
            FROM sessoes s 
            JOIN filmes f ON s.filme_id = f.id 
            JOIN cinemas c ON s.cinema_id = c.id 
            WHERE f.id = %s
        ''', (filme_id,))
        return self.cursor.fetchall()

    def get_assentos_disponiveis(self, sessao_id):
        self.cursor.execute("SELECT numero FROM assentos WHERE sessao_id = %s AND reservado = 0", (sessao_id,))
        return [row[0] for row in self.cursor.fetchall()]

    def get_lotacao_atual(self, sessao_id):
        self.cursor.execute("SELECT COUNT(*) FROM assentos WHERE sessao_id = %s AND reservado = 1", (sessao_id,))
        ocupados = self.cursor.fetchone()[0]
        self.cursor.execute("SELECT lotacao_maxima FROM sessoes WHERE id = %s", (sessao_id,))
        maxima = self.cursor.fetchone()[0]
        return ocupados, maxima

    def reservar_assentos(self, usuario_id, sessao_id, assentos_tipos, forma_pagamento):
        usuario_id = self._ensure_scalar(usuario_id)
        # Obter o preço base da sessão
        self.cursor.execute('SELECT preco FROM sessoes WHERE id = %s', (sessao_id,))
        preco_base = self.cursor.fetchone()[0]
        
        # Calcular o valor total com base nos tipos de ingressos
        valor_total = 0
        for assento_id, tipo_ingresso_id in assentos_tipos:
            self.cursor.execute('SELECT desconto_percentual FROM tipos_ingresso WHERE id = %s', (tipo_ingresso_id,))
            desconto = self.cursor.fetchone()[0]
            valor_ingresso = preco_base * (1 - desconto / 100)
            valor_total += valor_ingresso
        
        # Verificar lotação
        ocupados, maxima = self.get_lotacao_atual(sessao_id)
        if ocupados + len(assentos_tipos) > maxima:
            return False, "Sala lotada!"
        
        # Inserir reservas
        for assento_id, tipo_ingresso_id in assentos_tipos:
            self.cursor.execute('''
                INSERT INTO reservas (usuario_id, sessao_id, assento_id, tipo_ingresso_id, forma_pagamento, valor_total)
                VALUES (%s, %s, %s, %s, %s, %s)
            ''', (usuario_id, sessao_id, assento_id, tipo_ingresso_id, forma_pagamento, valor_total))
        
        self.conn.commit()
        return True, "Reserva realizada com sucesso!"

    def is_favorito(self, usuario_id, filme_id):
            """Verifica se o filme já está nos favoritos do usuário."""
            usuario_id = self._ensure_scalar(usuario_id)
            self.cursor.execute("SELECT COUNT(*) FROM favoritos WHERE usuario_id = %s AND filme_id = %s", (usuario_id, filme_id))
            return self.cursor.fetchone()[0] > 0

    def adicionar_favorito(self, usuario_id, filme_id):
            """Adiciona o filme aos favoritos se ele ainda não estiver favoritado."""
            usuario_id = self._ensure_scalar(usuario_id)
            if self.is_favorito(usuario_id, filme_id):
                return False, "O filme já está nos favoritos!"
            try:
                self.cursor.execute("INSERT INTO favoritos (usuario_id, filme_id) VALUES (%s, %s)", (usuario_id, filme_id))
                self.conn.commit()
                print(f"Filme {filme_id} adicionado aos favoritos do usuário {usuario_id}")
                return True, "Filme adicionado aos favoritos!"
            except Exception as e:
                print(f"Erro ao adicionar favorito: {str(e)}")
                return False, f"Erro ao adicionar favorito: {str(e)}"

    def remover_favorito(self, usuario_id, filme_id):
            """Remove o filme dos favoritos se ele estiver favoritado."""
            usuario_id = self._ensure_scalar(usuario_id)
            if not self.is_favorito(usuario_id, filme_id):
                return False, "O filme não está nos favoritos!"
            try:
                self.cursor.execute("DELETE FROM favoritos WHERE usuario_id = %s AND filme_id = %s", (usuario_id, filme_id))
                self.conn.commit()
                print(f"Filme {filme_id} removido dos favoritos do usuário {usuario_id}")
                return True, "Filme removido dos favoritos!"
            except Exception as e:
                print(f"Erro ao remover favorito: {str(e)}")
                return False, f"Erro ao remover favorito: {str(e)}"

    def get_favoritos(self, usuario_id):
        usuario_id = self._ensure_scalar(usuario_id)
        self.cursor.execute("""
            SELECT f.id, f.nome, f.cinema_id, f.duracao, f.data_lancamento, f.genero, f.classificacao, f.sinopse, f.trailer_url, f.poster_data 
            FROM filmes f 
            JOIN favoritos fav ON f.id = fav.filme_id 
            WHERE fav.usuario_id = %s
        """, (usuario_id,))
        favoritos = self.cursor.fetchall()
        return favoritos

    def get_compras(self, usuario_id):
        usuario_id = self._ensure_scalar(usuario_id)
        self.cursor.execute('''
            SELECT r.id, f.nome, s.data, s.horario, s.tipo_sala, c.nome, a.numero
            FROM reservas r
            JOIN sessoes s ON r.sessao_id = s.id
            JOIN filmes f ON s.filme_id = f.id
            JOIN cinemas c ON s.cinema_id = c.id
            JOIN assentos a ON r.assento_id = a.id
            WHERE r.usuario_id = %s
        ''', (usuario_id,))
        return self.cursor.fetchall()

    def fechar_conexao(self):
        self.db.fechar_conexao()

    def mensagem_ok(self,titulo,mensagem):
        self.titulo = titulo
        self.mensagem = mensagem
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(f"{titulo}")
        msg_box.setText(f"{mensagem}")
        msg_box.setStyleSheet("""
            QMessageBox {
                background-color: #2a2a2a;
                color: #ffffff;
            }
            QMessageBox QLabel {
                background-color: #2a2a2a;
                color: #ffffff;
            }
            QMessageBox QPushButton {
                background-color: #ffffff;
                color: #000000;
                width: 70px;
                height: 30px;
                border-radius: 8px;
            }
            QMessageBox QPushButton:hover {
                background-color: #999999;
            }
        """)
        msg_box.exec()

    def center_window(window):
        # Obter a geometria da tela principal
        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        screen_center = screen_geometry.center()

        # Obter a geometria da janela
        window_geometry = window.frameGeometry()
        window_center = window_geometry.center()

        # Calcular a nova posição para centralizar
        new_x = screen_center.x() - window_geometry.width() // 2
        new_y = screen_center.y() - window_geometry.height() // 2

        # Mover a janela para o centro
        window.move(new_x, new_y)

    def get_cinemas_all(self):
            self.cursor.execute("SELECT id, nome FROM cinemas")
            return self.cursor.fetchall()

    def adicionar_cinema(self, nome):
        try:
            self.cursor.execute("INSERT INTO cinemas (nome) VALUES (%s)", (nome,))
            self.conn.commit()
            return True, f"Cinema '{nome}' adicionado com sucesso!"
        except Exception as e:
            return False, f"Erro ao adicionar cinema: {str(e)}"

    def adicionar_filme(self, nome, cinema_id, duracao, data_lancamento, genero, classificacao, sinopse, trailer_url, poster_url):
        try:
            import requests
            poster_data = None
            if poster_url:
                response = requests.get(poster_url, timeout=5)
                response.raise_for_status()
                poster_data = response.content

            self.cursor.execute("""
                INSERT INTO filmes (nome, cinema_id, duracao, data_lancamento, genero, classificacao, sinopse, trailer_url, poster_data)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (nome, cinema_id, duracao, data_lancamento, genero, classificacao, sinopse, trailer_url, poster_data))
            self.conn.commit()
            return True, f"Filme '{nome}' adicionado com sucesso!"
        except Exception as e:
            return False, f"Erro ao adicionar filme: {str(e)}"

    def get_sessoes_all(self):
        self.cursor.execute("SELECT id, filme_id, cinema_id, data, horario, tipo_sala, lotacao_maxima, preco FROM sessoes")
        return self.cursor.fetchall()

    def adicionar_sessao(self, filme_id, cinema_id, data, horario, tipo_sala, lotacao_maxima, preco):
        try:
            self.cursor.execute("""
                INSERT INTO sessoes (filme_id, cinema_id, data, horario, tipo_sala, lotacao_maxima, preco)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (filme_id, cinema_id, data, horario, tipo_sala, lotacao_maxima, preco))
            sessao_id = self.cursor.lastrowid

            # Criar assentos automaticamente
            for i in range(1, lotacao_maxima + 1):
                self.cursor.execute("INSERT INTO assentos (sessao_id, numero, reservado) VALUES (%s, %s, %s)",
                                    (sessao_id, f"A{i:02d}", 0))
            self.conn.commit()
            return True, f"Sessão adicionada com sucesso! Preço: R${preco:.2f}"
        except Exception as e:
            self.conn.rollback()
            return False, f"Erro ao adicionar sessão: {str(e)}"
        
# Método auxiliar para obter o preço de uma sessão específica
    def get_preco_sessao(self, sessao_id):
        self.cursor.execute("SELECT preco FROM sessoes WHERE id = %s", (sessao_id,))
        result = self.cursor.fetchone()
        return result[0] if result else 20.00  # Valor padrão caso não encontre
    
    def get_tipos_ingresso(self):
        self.cursor.execute('SELECT id, nome, desconto_percentual FROM tipos_ingresso')
        return self.cursor.fetchall()