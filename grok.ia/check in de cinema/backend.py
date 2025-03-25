# backend.py
import mysql.connector
from database import CinemaDatabase

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

    def reservar_assentos(self, usuario_id, sessao_id, assentos, forma_pagamento):
        usuario_id = self._ensure_scalar(usuario_id)
        ocupados, maxima = self.get_lotacao_atual(sessao_id)
        print(f"Lotação atual: {ocupados}/{maxima}, Tentando reservar {len(assentos)} assentos")
        if ocupados + len(assentos) > maxima:
            return False, "Sala lotada!"

        valor_total = len(assentos) * 20.0
        try:
            for assento in assentos:
                self.cursor.execute("UPDATE assentos SET reservado = 1 WHERE sessao_id = %s AND numero = %s AND reservado = 0", (sessao_id, assento))
                if self.cursor.rowcount == 0:
                    raise Exception(f"Assento {assento} já reservado ou não existe!")
                self.cursor.execute("SELECT id FROM assentos WHERE sessao_id = %s AND numero = %s", (sessao_id, assento))
                assento_id = self.cursor.fetchone()
                if assento_id:
                    assento_id = assento_id[0]
                    self.cursor.execute("INSERT INTO reservas (usuario_id, sessao_id, assento_id, forma_pagamento, valor_total) VALUES (%s, %s, %s, %s, %s)",
                                        (usuario_id, sessao_id, assento_id, forma_pagamento, valor_total / len(assentos)))
                else:
                    raise Exception(f"Assento {assento} não encontrado para sessão {sessao_id}")
            self.conn.commit()
            return True, f"Compra concluída! Valor total: R${valor_total:.2f}"
        except Exception as e:
            self.conn.rollback()
            print(f"Erro ao reservar assentos: {e}")
            return False, f"Erro ao realizar compra: {str(e)}"

    def adicionar_favorito(self, usuario_id, filme_id):
        usuario_id = self._ensure_scalar(usuario_id)
        try:
            self.cursor.execute("INSERT INTO favoritos (usuario_id, filme_id) VALUES (%s, %s)", (usuario_id, filme_id))
            self.conn.commit()
            print(f"Filme {filme_id} adicionado aos favoritos do usuário {usuario_id}")
            return True, "Filme adicionado aos favoritos!"
        except Exception as e:
            print(f"Erro ao adicionar favorito: {str(e)}")
            return False, f"Erro ao adicionar favorito: {str(e)}"

    def remover_favorito(self, usuario_id, filme_id):
        usuario_id = self._ensure_scalar(usuario_id)
        self.cursor.execute("DELETE FROM favoritos WHERE usuario_id = %s AND filme_id = %s", (usuario_id, filme_id))
        self.conn.commit()

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