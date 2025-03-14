# backend.py
import sqlite3

class CinemaBackend:
    def __init__(self):
        self.conn = sqlite3.connect('cinema.db')
        self.cursor = self.conn.cursor()

    def cadastrar_usuario(self, nome, sobrenome, email, senha):
        try:
            self.cursor.execute("INSERT INTO usuarios (nome, sobrenome, email, senha) VALUES (?, ?, ?, ?)", 
                                (nome, sobrenome, email, senha))
            self.conn.commit()
            return True, "Cadastro realizado com sucesso!"
        except sqlite3.IntegrityError:
            return False, "E-mail já cadastrado!"

    def login(self, nome, senha):
        self.cursor.execute("SELECT id, nome FROM usuarios WHERE nome = ? AND senha = ?", (nome, senha))
        usuario = self.cursor.fetchone()
        if usuario:
            return True, usuario[0], usuario[1]
        return False, None, "Nome ou senha incorretos!"

    def get_usuario_info(self, usuario_id):
        self.cursor.execute("SELECT nome, sobrenome, email, senha FROM usuarios WHERE id = ?", (usuario_id,))
        return self.cursor.fetchone()

    def get_cartao_info(self, usuario_id):
        self.cursor.execute("SELECT nome_cartao, numero_cartao, data_expiracao, cvv FROM cartoes WHERE usuario_id = ?", (usuario_id,))
        return self.cursor.fetchone()

    def salvar_cartao(self, usuario_id, nome_cartao, numero_cartao, data_expiracao, cvv):
        self.cursor.execute("INSERT OR REPLACE INTO cartoes (usuario_id, nome_cartao, numero_cartao, data_expiracao, cvv) VALUES (?, ?, ?, ?, ?)", 
                            (usuario_id, nome_cartao, numero_cartao, data_expiracao, cvv))
        self.conn.commit()

    def get_filmes_all(self):
        self.cursor.execute("SELECT * FROM filmes")
        return self.cursor.fetchall()

    def get_filme_info(self, filme_id):
        self.cursor.execute("SELECT * FROM filmes WHERE id = ?", (filme_id,))
        return self.cursor.fetchone()

    def get_sessoes_info(self, filme_id):
        self.cursor.execute('''
            SELECT s.id, s.data, s.horario, s.tipo_sala, c.nome 
            FROM sessoes s 
            JOIN filmes f ON s.filme_id = f.id 
            JOIN cinemas c ON f.cinema_id = c.id 
            WHERE f.id = ?
        ''', (filme_id,))
        return self.cursor.fetchall()

    def get_assentos_disponiveis(self, sessao_id):
        self.cursor.execute("SELECT numero FROM assentos WHERE sessao_id = ? AND reservado = 0", (sessao_id,))
        return [row[0] for row in self.cursor.fetchall()]

    def get_lotacao_atual(self, sessao_id):
        self.cursor.execute("SELECT COUNT(*) FROM assentos WHERE sessao_id = ? AND reservado = 1", (sessao_id,))
        ocupados = self.cursor.fetchone()[0]
        self.cursor.execute("SELECT lotacao_maxima FROM sessoes WHERE id = ?", (sessao_id,))
        maxima = self.cursor.fetchone()[0]
        return ocupados, maxima

    def reservar_assentos(self, usuario_id, sessao_id, assentos, forma_pagamento):
        ocupados, maxima = self.get_lotacao_atual(sessao_id)
        if ocupados + len(assentos) > maxima:
            return False, "Sala lotada!"

        valor_total = len(assentos) * 20.0  # Preço fixo por ingresso
        for assento in assentos:
            self.cursor.execute("UPDATE assentos SET reservado = 1 WHERE sessao_id = ? AND numero = ?", (sessao_id, assento))
            self.cursor.execute("SELECT id FROM assentos WHERE sessao_id = ? AND numero = ?", (sessao_id, assento))
            assento_id = self.cursor.fetchone()[0]
            self.cursor.execute("INSERT INTO reservas (usuario_id, sessao_id, assento_id, forma_pagamento, valor_total) VALUES (?, ?, ?, ?, ?)",
                                (usuario_id, sessao_id, assento_id, forma_pagamento, valor_total / len(assentos)))
        
        self.conn.commit()
        return True, f"Compra concluída! Valor total: R${valor_total:.2f}"

    def adicionar_favorito(self, usuario_id, filme_id):
        self.cursor.execute("INSERT INTO favoritos (usuario_id, filme_id) VALUES (?, ?)", (usuario_id, filme_id))
        self.conn.commit()

    def remover_favorito(self, usuario_id, filme_id):
        self.cursor.execute("DELETE FROM favoritos WHERE usuario_id = ? AND filme_id = ?", (usuario_id, filme_id))
        self.conn.commit()

    def get_favoritos(self, usuario_id):
        self.cursor.execute("SELECT f.* FROM filmes f JOIN favoritos fav ON f.id = fav.filme_id WHERE fav.usuario_id = ?", (usuario_id,))
        return self.cursor.fetchall()

    def get_compras(self, usuario_id):
        self.cursor.execute('''
            SELECT r.id, f.nome, s.data, s.horario, s.tipo_sala, c.nome, a.numero
            FROM reservas r
            JOIN sessoes s ON r.sessao_id = s.id
            JOIN filmes f ON s.filme_id = f.id
            JOIN cinemas c ON f.cinema_id = c.id
            JOIN assentos a ON r.assento_id = a.id
            WHERE r.usuario_id = ?
        ''', (usuario_id,))
        return self.cursor.fetchall()

    def __del__(self):
        self.conn.close()