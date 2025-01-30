import sys
import sqlite3
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QComboBox, QMessageBox

class CinemaApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema de Check-In do Cinema")
        self.setGeometry(100, 100, 600, 400)
        
        self.layout = QVBoxLayout()
        
        # Rótulo e combo box para selecionar o cinema
        self.cinema_label = QLabel("Escolha um Cinema:")
        self.layout.addWidget(self.cinema_label)
        
        self.cinema_combo = QComboBox()
        self.load_cinemas()
        self.layout.addWidget(self.cinema_combo)
        
        # Rótulo e combo box para selecionar o filme
        self.movie_label = QLabel("Escolha um Filme:")
        self.layout.addWidget(self.movie_label)
        
        self.movie_combo = QComboBox()
        self.layout.addWidget(self.movie_combo)
        
        # Rótulo e combo box para selecionar a data
        self.date_label = QLabel("Escolha uma Data:")
        self.layout.addWidget(self.date_label)
        
        self.date_combo = QComboBox()
        self.layout.addWidget(self.date_combo)
        
        # Rótulo e combo box para selecionar o horário
        self.time_label = QLabel("Escolha um Horário:")
        self.layout.addWidget(self.time_label)
        
        self.time_combo = QComboBox()
        self.layout.addWidget(self.time_combo)
        
        # Botão para selecionar a sessão
        self.select_button = QPushButton("Selecionar Sessão")
        self.select_button.clicked.connect(self.select_session)
        self.layout.addWidget(self.select_button)

        # Rótulo e combo box para selecionar o método de pagamento
        self.payment_label = QLabel("Escolha um Método de Pagamento:")
        self.layout.addWidget(self.payment_label)

        self.payment_combo = QComboBox()
        self.payment_combo.addItems(["Cartão de Crédito", "Cartão de Débito", "Pix", "Boleto"])
        self.layout.addWidget(self.payment_combo)

        # Botão para confirmar o pagamento
        self.confirm_button = QPushButton("Confirmar Pagamento")
        self.confirm_button.clicked.connect(self.confirm_payment)
        self.layout.addWidget(self.confirm_button)
        
        self.setLayout(self.layout)

    # Método para carregar os cinemas do banco de dados
    def load_cinemas(self):
        conn = sqlite3.connect('cinema.db')
        cursor = conn.cursor()
        cursor.execute("SELECT nome FROM cinemas")
        cinemas = cursor.fetchall()
        for cinema in cinemas:
            self.cinema_combo.addItem(cinema[0])
        conn.close()

    # Método para carregar os filmes com base no cinema selecionado
    def load_movies(self):
        selected_cinema = self.cinema_combo.currentText()
        conn = sqlite3.connect('cinema.db')
        cursor = conn.cursor()
        cursor.execute("SELECT nome FROM filmes WHERE cinema_id = (SELECT id FROM cinemas WHERE nome = ?)", (selected_cinema,))
        movies = cursor.fetchall()
        self.movie_combo.clear()
        for movie in movies:
            self.movie_combo.addItem(movie[0])
        conn.close()

    # Método para carregar as datas disponíveis (ainda não implementado)
    def load_dates(self):
        pass

    # Método para carregar os horários disponíveis (ainda não implementado)
    def load_times(self):
        pass

    # Método para selecionar uma sessão e exibir as informações
    def select_session(self):
        selected_cinema = self.cinema_combo.currentText()
        selected_movie = self.movie_combo.currentText()
        selected_date = self.date_combo.currentText()
        selected_time = self.time_combo.currentText()
        QMessageBox.information(self, "Sessão Selecionada", f"Cinema: {selected_cinema}\nFilme: {selected_movie}\nData: {selected_date}\nHorário: {selected_time}")

    # Método para confirmar o pagamento e exibir as informações
    def confirm_payment(self):
        selected_payment = self.payment_combo.currentText()
        QMessageBox.information(self, "Pagamento Confirmado", f"Método de Pagamento: {selected_payment}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CinemaApp()
    window.show()
    sys.exit(app.exec())
