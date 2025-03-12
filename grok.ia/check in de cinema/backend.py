# backend.py
import sqlite3

class CinemaBackend:
    def __init__(self):
        self.conn = sqlite3.connect('cinema.db')
        self.cursor = self.conn.cursor()

    def get_cinemas(self):
        self.cursor.execute("SELECT * FROM cinemas")
        return self.cursor.fetchall()

    def get_filmes(self, cinema_id):
        self.cursor.execute("SELECT * FROM filmes WHERE cinema_id = ?", (cinema_id,))
        return self.cursor.fetchall()

    def get_filmes_all(self):
        self.cursor.execute("SELECT * FROM filmes")
        return self.cursor.fetchall()

    def get_sessoes(self, filme_id):
        self.cursor.execute("SELECT * FROM sessoes WHERE filme_id = ?", (filme_id,))
        return self.cursor.fetchall()

    def get_sessoes_info(self, filme_id):
        self.cursor.execute('''
            SELECT s.id, s.data, s.horario, c.nome 
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

    def reservar_assentos(self, sessao_id, assentos, forma_pagamento):
        ocupados, maxima = self.get_lotacao_atual(sessao_id)
        if ocupados + len(assentos) > maxima:
            return False, "Sala lotada!"

        valor_total = len(assentos) * 20.0  # Preço fixo por ingresso (exemplo)
        for assento in assentos:
            self.cursor.execute("UPDATE assentos SET reservado = 1 WHERE sessao_id = ? AND numero = ?", (sessao_id, assento))
            self.cursor.execute("SELECT id FROM assentos WHERE sessao_id = ? AND numero = ?", (sessao_id, assento))
            assento_id = self.cursor.fetchone()[0]
            self.cursor.execute("INSERT INTO reservas (sessao_id, assento_id, forma_pagamento, valor_total) VALUES (?, ?, ?, ?)",
                                (sessao_id, assento_id, forma_pagamento, valor_total / len(assentos)))
        
        self.conn.commit()
        return True, f"Reserva concluída! Valor total: R${valor_total:.2f}"

    def __del__(self):
        self.conn.close()