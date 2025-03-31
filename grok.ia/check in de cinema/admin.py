# admin.py
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QComboBox, QDialog, QMessageBox, QScrollArea
from PySide6.QtCore import Qt
from backend import CinemaBackend

class AdminWindow(QMainWindow):
    def __init__(self, backend, parent=None):
        super().__init__(parent)
        self.backend = backend
        self.setWindowTitle("Painel do Administrador - PobreVision")
        self.setMinimumSize(800, 600)
        self.init_ui()

    def init_ui(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)

        # Barra de navegação
        self.nav_bar = QHBoxLayout()
        self.nav_bar.addWidget(self.create_nav_button("🏢 Gerenciar Cinemas", self.show_cinemas))
        self.nav_bar.addWidget(self.create_nav_button("🎥 Gerenciar Filmes", self.show_filmes))
        self.nav_bar.addWidget(self.create_nav_button("📅 Gerenciar Sessões", self.show_sessoes))
        self.nav_bar.addWidget(self.create_nav_button("🚪 Sair", self.logout))
        self.main_layout.addLayout(self.nav_bar)

        # Área de conteúdo
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.main_layout.addWidget(self.content_widget)

        # Estilo geral
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1a1a1a;
            }
            QLabel {
                color: #ffffff;
                font-size: 16px;
                font-family: Arial, sans-serif;
            }
        """)

        # Exibir a tela inicial (Cinemas por padrão)
        self.show_cinemas()

    def create_nav_button(self, text, callback):
        btn = QPushButton(text)
        btn.setStyleSheet("""
            QPushButton {
                background-color: #e50914;
                color: #ffffff;
                padding: 10px 20px;
                border-radius: 8px;
                border: 1px solid #ffffff;
                font-size: 14px;
                font-family: Arial, sans-serif;
            }
            QPushButton:hover {
                background-color: #a34045;
                border: 1px solid #ffffff;
            }
            QPushButton:pressed {
                background-color: #8b2f34;
            }
        """)
        btn.clicked.connect(callback)
        return btn

    def clear_content(self):
        for i in reversed(range(self.content_layout.count())):
            widget = self.content_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

    def show_cinemas(self):
        self.clear_content()
        scroll = QScrollArea()
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll.setWidget(scroll_content)
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("background-color: transparent; border: none;")

        scroll_layout.addWidget(QLabel("Gerenciar Cinemas"))
        add_cinema_btn = QPushButton("Adicionar Cinema")
        add_cinema_btn.setStyleSheet("""
            QPushButton {
                background-color: #e50914;
                color: #ffffff;
                padding: 10px 20px;
                border-radius: 8px;
                border: 1px solid #ffffff;
                font-size: 14px;
                font-family: Arial, sans-serif;
            }
            QPushButton:hover {
                background-color: #a34045;
                border: 1px solid #ffffff;
            }
            QPushButton:pressed {
                background-color: #8b2f34;
            }
        """)
        add_cinema_btn.clicked.connect(self.abrir_add_cinema)
        scroll_layout.addWidget(add_cinema_btn)

        cinemas = self.backend.get_cinemas_all()
        for cinema in cinemas:
            cinema_label = QLabel(f"ID: {cinema[0]} - Nome: {cinema[1]}")
            scroll_layout.addWidget(cinema_label)

        self.content_layout.addWidget(scroll)

    def show_filmes(self):
        self.clear_content()
        scroll = QScrollArea()
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll.setWidget(scroll_content)
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("background-color: transparent; border: none;")

        scroll_layout.addWidget(QLabel("Gerenciar Filmes"))
        add_filme_btn = QPushButton("Adicionar Filme")
        add_filme_btn.setStyleSheet("""
            QPushButton {
                background-color: #e50914;
                color: #ffffff;
                padding: 10px 20px;
                border-radius: 8px;
                border: 1px solid #ffffff;
                font-size: 14px;
                font-family: Arial, sans-serif;
            }
            QPushButton:hover {
                background-color: #a34045;
                border: 1px solid #ffffff;
            }
            QPushButton:pressed {
                background-color: #8b2f34;
            }
        """)
        add_filme_btn.clicked.connect(self.abrir_add_filme)
        scroll_layout.addWidget(add_filme_btn)

        filmes = self.backend.get_filmes_all()
        for filme in filmes:
            filme_label = QLabel(f"ID: {filme[0]} - Nome: {filme[1]} - Cinema ID: {filme[2]}")
            scroll_layout.addWidget(filme_label)

        self.content_layout.addWidget(scroll)

    def show_sessoes(self):
        self.clear_content()
        scroll = QScrollArea()
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll.setWidget(scroll_content)
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("background-color: transparent; border: none;")

        scroll_layout.addWidget(QLabel("Gerenciar Sessões"))
        add_sessao_btn = QPushButton("Adicionar Sessão")
        add_sessao_btn.setStyleSheet("""
            QPushButton {
                background-color: #e50914;
                color: #ffffff;
                padding: 10px 20px;
                border-radius: 8px;
                border: 1px solid #ffffff;
                font-size: 14px;
                font-family: Arial, sans-serif;
            }
            QPushButton:hover {
                background-color: #a34045;
                border: 1px solid #ffffff;
            }
            QPushButton:pressed {
                background-color: #8b2f34;
            }
        """)
        add_sessao_btn.clicked.connect(self.abrir_add_sessao)
        scroll_layout.addWidget(add_sessao_btn)

        sessoes = self.backend.get_sessoes_all()
        for sessao in sessoes:
            sessao_label = QLabel(f"ID: {sessao[0]} - Filme ID: {sessao[1]} - Cinema ID: {sessao[2]} - Data: {sessao[3]} - Horário: {sessao[4]} - Tipo Sala: {sessao[5]} - Lotação: {sessao[6]}")
            scroll_layout.addWidget(sessao_label)

        self.content_layout.addWidget(scroll)

    def abrir_add_cinema(self):
        dialog = AddCinemaDialog(self.backend, self)
        dialog.exec()

    def abrir_add_filme(self):
        dialog = AddFilmeDialog(self.backend, self)
        dialog.exec()

    def abrir_add_sessao(self):
        dialog = AddSessaoDialog(self.backend, self)
        dialog.exec()

    def logout(self):
        self.close()
        self.parent().show()

class AddCinemaDialog(QDialog):
    def __init__(self, backend, parent=None):
        super().__init__(parent)
        self.backend = backend
        self.setWindowTitle("Adicionar Cinema")
        self.setMinimumSize(400, 300)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.nome_input = QLineEdit()
        self.nome_input.setPlaceholderText("Nome do Cinema")
        self.nome_input.setStyleSheet("background-color: #333333; color: #ffffff; padding: 5px;")
        layout.addWidget(self.nome_input)

        salvar_btn = QPushButton("Salvar")
        salvar_btn.setStyleSheet("""
            QPushButton {
                background-color: #e50914;
                color: #ffffff;
                padding: 10px 20px;
                border-radius: 8px;
                border: 1px solid #ffffff;
                font-size: 14px;
                font-family: Arial, sans-serif;
            }
            QPushButton:hover {
                background-color: #a34045;
                border: 1px solid #ffffff;
            }
            QPushButton:pressed {
                background-color: #8b2f34;
            }
        """)
        salvar_btn.clicked.connect(self.salvar_cinema)
        layout.addWidget(salvar_btn)

        cancelar_btn = QPushButton("Cancelar")
        cancelar_btn.setStyleSheet("""
            QPushButton {
                background-color: #777777;
                color: #ffffff;
                padding: 10px 20px;
                border-radius: 8px;
                border: 1px solid #ffffff;
                font-size: 14px;
                font-family: Arial, sans-serif;
            }
            QPushButton:hover {
                background-color: #555555;
                border: 1px solid #ffffff;
            }
            QPushButton:pressed {
                background-color: #444444;
            }
        """)
        cancelar_btn.clicked.connect(self.close)
        layout.addWidget(cancelar_btn)

        self.setLayout(layout)
        self.setStyleSheet("background-color: #1a1a1a;")

    def salvar_cinema(self):
        nome = self.nome_input.text().strip()
        if not nome:
            QMessageBox.warning(self, "Erro", "O nome do cinema é obrigatório!")
            return
        sucesso, mensagem = self.backend.adicionar_cinema(nome)
        if sucesso:
            QMessageBox.information(self, "Sucesso", mensagem)
            self.close()
            self.parent().show_cinemas()
        else:
            QMessageBox.critical(self, "Erro", mensagem)

class AddFilmeDialog(QDialog):
    def __init__(self, backend, parent=None):
        super().__init__(parent)
        self.backend = backend
        self.setWindowTitle("Adicionar Filme")
        self.setMinimumSize(400, 500)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.nome_input = QLineEdit()
        self.nome_input.setPlaceholderText("Nome do Filme")
        self.nome_input.setStyleSheet("background-color: #333333; color: #ffffff; padding: 5px;")
        layout.addWidget(self.nome_input)

        self.cinema_combo = QComboBox()
        self.cinema_combo.setStyleSheet("background-color: #333333; color: #ffffff; padding: 5px;")
        cinemas = self.backend.get_cinemas_all()
        for cinema in cinemas:
            self.cinema_combo.addItem(cinema[1], cinema[0])
        layout.addWidget(self.cinema_combo)

        self.duracao_input = QLineEdit()
        self.duracao_input.setPlaceholderText("Duração (ex.: 01:30:00)")
        self.duracao_input.setStyleSheet("background-color: #333333; color: #ffffff; padding: 5px;")
        layout.addWidget(self.duracao_input)

        self.data_lancamento_input = QLineEdit()
        self.data_lancamento_input.setPlaceholderText("Data de Lançamento (ex.: 2023-01-01)")
        self.data_lancamento_input.setStyleSheet("background-color: #333333; color: #ffffff; padding: 5px;")
        layout.addWidget(self.data_lancamento_input)

        self.genero_input = QLineEdit()
        self.genero_input.setPlaceholderText("Gênero")
        self.genero_input.setStyleSheet("background-color: #333333; color: #ffffff; padding: 5px;")
        layout.addWidget(self.genero_input)

        self.classificacao_input = QLineEdit()
        self.classificacao_input.setPlaceholderText("Classificação (ex.: Livre, 12)")
        self.classificacao_input.setStyleSheet("background-color: #333333; color: #ffffff; padding: 5px;")
        layout.addWidget(self.classificacao_input)

        self.sinopse_input = QLineEdit()
        self.sinopse_input.setPlaceholderText("Sinopse")
        self.sinopse_input.setStyleSheet("background-color: #333333; color: #ffffff; padding: 5px;")
        layout.addWidget(self.sinopse_input)

        self.trailer_input = QLineEdit()
        self.trailer_input.setPlaceholderText("URL do Trailer")
        self.trailer_input.setStyleSheet("background-color: #333333; color: #ffffff; padding: 5px;")
        layout.addWidget(self.trailer_input)

        self.poster_input = QLineEdit()
        self.poster_input.setPlaceholderText("URL da Imagem do Pôster")
        self.poster_input.setStyleSheet("background-color: #333333; color: #ffffff; padding: 5px;")
        layout.addWidget(self.poster_input)

        salvar_btn = QPushButton("Salvar")
        salvar_btn.setStyleSheet("""
            QPushButton {
                background-color: #e50914;
                color: #ffffff;
                padding: 10px 20px;
                border-radius: 8px;
                border: 1px solid #ffffff;
                font-size: 14px;
                font-family: Arial, sans-serif;
            }
            QPushButton:hover {
                background-color: #a34045;
                border: 1px solid #ffffff;
            }
            QPushButton:pressed {
                background-color: #8b2f34;
            }
        """)
        salvar_btn.clicked.connect(self.salvar_filme)
        layout.addWidget(salvar_btn)

        cancelar_btn = QPushButton("Cancelar")
        cancelar_btn.setStyleSheet("""
            QPushButton {
                background-color: #777777;
                color: #ffffff;
                padding: 10px 20px;
                border-radius: 8px;
                border: 1px solid #ffffff;
                font-size: 14px;
                font-family: Arial, sans-serif;
            }
            QPushButton:hover {
                background-color: #555555;
                border: 1px solid #ffffff;
            }
            QPushButton:pressed {
                background-color: #444444;
            }
        """)
        cancelar_btn.clicked.connect(self.close)
        layout.addWidget(cancelar_btn)

        self.setLayout(layout)
        self.setStyleSheet("background-color: #1a1a1a;")

    def salvar_filme(self):
        nome = self.nome_input.text().strip()
        cinema_id = self.cinema_combo.currentData()
        duracao = self.duracao_input.text().strip()
        data_lancamento = self.data_lancamento_input.text().strip()
        genero = self.genero_input.text().strip()
        classificacao = self.classificacao_input.text().strip()
        sinopse = self.sinopse_input.text().strip()
        trailer_url = self.trailer_input.text().strip()
        poster_url = self.poster_input.text().strip()

        if not all([nome, duracao, data_lancamento, genero, classificacao, sinopse, trailer_url, poster_url]):
            QMessageBox.warning(self, "Erro", "Todos os campos são obrigatórios!")
            return

        sucesso, mensagem = self.backend.adicionar_filme(nome, cinema_id, duracao, data_lancamento, genero, classificacao, sinopse, trailer_url, poster_url)
        if sucesso:
            QMessageBox.information(self, "Sucesso", mensagem)
            self.close()
            self.parent().show_filmes()
        else:
            QMessageBox.critical(self, "Erro", mensagem)

class AddSessaoDialog(QDialog):
    def __init__(self, backend, parent=None):
        super().__init__(parent)
        self.backend = backend
        self.setWindowTitle("Adicionar Sessão")
        self.setMinimumSize(400, 400)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.filme_combo = QComboBox()
        self.filme_combo.setStyleSheet("background-color: #333333; color: #ffffff; padding: 5px;")
        filmes = self.backend.get_filmes_all()
        for filme in filmes:
            self.filme_combo.addItem(filme[1], filme[0])
        layout.addWidget(self.filme_combo)

        self.cinema_combo = QComboBox()
        self.cinema_combo.setStyleSheet("background-color: #333333; color: #ffffff; padding: 5px;")
        cinemas = self.backend.get_cinemas_all()
        for cinema in cinemas:
            self.cinema_combo.addItem(cinema[1], cinema[0])
        layout.addWidget(self.cinema_combo)

        self.data_input = QLineEdit()
        self.data_input.setPlaceholderText("Data (ex.: 2025-03-15)")
        self.data_input.setStyleSheet("background-color: #333333; color: #ffffff; padding: 5px;")
        layout.addWidget(self.data_input)

        self.horario_input = QLineEdit()
        self.horario_input.setPlaceholderText("Horário (ex.: 14:00:00)")
        self.horario_input.setStyleSheet("background-color: #333333; color: #ffffff; padding: 5px;")
        layout.addWidget(self.horario_input)

        self.tipo_sala_input = QComboBox()
        self.tipo_sala_input.setStyleSheet("background-color: #333333; color: #ffffff; padding: 5px;")
        self.tipo_sala_input.addItems(["Convencional", "IMAX", "3D", "VIP", "Drive-in"])
        layout.addWidget(self.tipo_sala_input)

        self.lotacao_input = QLineEdit()
        self.lotacao_input.setPlaceholderText("Lotação Máxima (ex.: 50)")
        self.lotacao_input.setStyleSheet("background-color: #333333; color: #ffffff; padding: 5px;")
        layout.addWidget(self.lotacao_input)

        self.preco_input = QLineEdit()
        self.preco_input.setPlaceholderText("Preço do Ingresso (ex.: 20.00)")
        self.preco_input.setStyleSheet("background-color: #333333; color: #ffffff; padding: 5px;")
        layout.addWidget(self.preco_input)

        salvar_btn = QPushButton("Salvar")
        salvar_btn.setStyleSheet("""
            QPushButton {
                background-color: #e50914;
                color: #ffffff;
                padding: 10px 20px;
                border-radius: 8px;
                border: 1px solid #ffffff;
                font-size: 14px;
                font-family: Arial, sans-serif;
            }
            QPushButton:hover {
                background-color: #a34045;
                border: 1px solid #ffffff;
            }
            QPushButton:pressed {
                background-color: #8b2f34;
            }
        """)
        salvar_btn.clicked.connect(self.salvar_sessao)
        layout.addWidget(salvar_btn)

        cancelar_btn = QPushButton("Cancelar")
        cancelar_btn.setStyleSheet("""
            QPushButton {
                background-color: #777777;
                color: #ffffff;
                padding: 10px 20px;
                border-radius: 8px;
                border: 1px solid #ffffff;
                font-size: 14px;
                font-family: Arial, sans-serif;
            }
            QPushButton:hover {
                background-color: #555555;
                border: 1px solid #ffffff;
            }
            QPushButton:pressed {
                background-color: #444444;
            }
        """)
        cancelar_btn.clicked.connect(self.close)
        layout.addWidget(cancelar_btn)

        self.setLayout(layout)
        self.setStyleSheet("background-color: #1a1a1a;")

    def salvar_sessao(self):
        filme_id = self.filme_combo.currentData()
        cinema_id = self.cinema_combo.currentData()
        data = self.data_input.text().strip()
        horario = self.horario_input.text().strip()
        tipo_sala = self.tipo_sala_input.currentText()
        lotacao_maxima = self.lotacao_input.text().strip()
        preco = self.preco_input.text().strip()

        if not all([filme_id, cinema_id, data, horario, tipo_sala, lotacao_maxima, preco]):
            QMessageBox.warning(self, "Erro", "Todos os campos são obrigatórios!")
            return

        try:
            lotacao_maxima = int(lotacao_maxima)
            preco = float(preco)
        except ValueError:
            QMessageBox.warning(self, "Erro", "Lotação máxima deve ser um número inteiro e preço um valor numérico!")
            return

        sucesso, mensagem = self.backend.adicionar_sessao(filme_id, cinema_id, data, horario, tipo_sala, lotacao_maxima, preco)
        if sucesso:
            QMessageBox.information(self, "Sucesso", mensagem)
            self.close()
            self.parent().show_sessoes()
        else:
            QMessageBox.critical(self, "Erro", mensagem)