# frontend.py
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QComboBox, QPushButton, QLabel, QListWidget, QLineEdit, QMessageBox, QScrollArea, QGridLayout, QDialog
from PySide6.QtCore import Qt, QSize
from backend import CinemaBackend
import sys

class FilmeInfoWindow(QDialog):
    def __init__(self, backend, filme_id, parent=None):
        super().__init__(parent)
        self.backend = backend
        self.filme_id = filme_id
        self.setWindowTitle("Informações do Filme")
        self.setStyleSheet("""
            QDialog {
                background-color: #1a1a1a;
            }
            QLabel {
                color: #ffffff;
                font-size: 16px;
                font-family: Arial, sans-serif;
            }
            QPushButton {
                background-color: #e50914;
                color: #ffffff;
                border-radius: 8px;
                padding: 8px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #f40612;
            }
            QListWidget {
                background-color: #2a2a2a;
                color: #ffffff;
                border: 1px solid #444;
                border-radius: 8px;
            }
        """)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        # Título do Filme
        self.filme_info = self.backend.get_filmes_all()
        filme_nome = next((f[1] for f in self.filme_info if f[0] == self.filme_id), "Filme Não Encontrado")
        title_label = QLabel(f"Filme: {filme_nome}")
        title_label.setStyleSheet("font-size: 20px; font-weight: bold; padding: 10px;")
        layout.addWidget(title_label)

        # Lista de Sessões (Cinema, Dia, Horário)
        self.sessao_list = QListWidget()
        sessoes_info = self.backend.get_sessoes_info(self.filme_id)
        for sessao in sessoes_info:
            sessao_id, data, horario, cinema_nome = sessao
            self.sessao_list.addItem(f"{cinema_nome} - {data} às {horario}")
        self.sessao_list.itemClicked.connect(self.on_sessao_selected)
        layout.addWidget(self.sessao_list)

        # Botão de Compra
        self.comprar_btn = QPushButton("Comprar Ingresso")
        self.comprar_btn.clicked.connect(self.abrir_compra)
        self.comprar_btn.setEnabled(False)  # Desabilitado até selecionar uma sessão
        layout.addWidget(self.comprar_btn)

        self.setFixedSize(400, 300)

    def on_sessao_selected(self, item):
        self.selected_sessao_id = int(item.text().split(" - ")[0].split(" ")[0])  # Extrair ID da sessão
        self.comprar_btn.setEnabled(True)

    def abrir_compra(self):
        if hasattr(self, 'selected_sessao_id'):
            self.compra_window = CompraWindow(self.backend, self.selected_sessao_id, self)
            self.compra_window.exec()
        else:
            QMessageBox.warning(self, "Erro", "Selecione uma sessão primeiro!")

class CompraWindow(QDialog):
    def __init__(self, backend, sessao_id, parent=None):
        super().__init__(parent)
        self.backend = backend
        self.sessao_id = sessao_id
        self.setWindowTitle("Compra de Ingresso")
        self.setStyleSheet("""
            QDialog {
                background-color: #1a1a1a;
            }
            QLabel {
                color: #ffffff;
                font-size: 16px;
                font-family: Arial, sans-serif;
            }
            QLineEdit, QPushButton {
                background-color: #2a2a2a;
                color: #ffffff;
                border: 1px solid #444;
                border-radius: 8px;
                padding: 8px;
                font-size: 14px;
            }
            QPushButton {
                background-color: #e50914;
            }
            QPushButton:hover {
                background-color: #f40612;
            }
            QListWidget {
                background-color: #2a2a2a;
                color: #ffffff;
                border: 1px solid #444;
                border-radius: 8px;
            }
        """)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        # Assentos Disponíveis
        self.assentos_list = QListWidget()
        self.assentos_list.setSelectionMode(QListWidget.MultiSelection)
        assentos = self.backend.get_assentos_disponiveis(self.sessao_id)
        self.assentos_list.addItems(assentos)
        layout.addWidget(QLabel("Assentos Disponíveis:"))
        layout.addWidget(self.assentos_list)

        # Quantidade de Ingressos
        self.qtd_ingressos = QLineEdit()
        self.qtd_ingressos.setPlaceholderText("Quantos ingressos?")
        layout.addWidget(QLabel("Quantidade de Ingressos:"))
        layout.addWidget(self.qtd_ingressos)

        # Forma de Pagamento
        self.pagamento_combo = QComboBox()
        self.pagamento_combo.addItems(["Cartão de Crédito/Débito", "PIX", "Boleto"])
        layout.addWidget(QLabel("Forma de Pagamento:"))
        layout.addWidget(self.pagamento_combo)

        # Botão de Confirmar Compra
        self.confirmar_btn = QPushButton("Confirmar Compra")
        self.confirmar_btn.clicked.connect(self.fazer_reserva)
        layout.addWidget(self.confirmar_btn)

        self.setFixedSize(400, 300)

    def fazer_reserva(self):
        assentos_selecionados = [item.text() for item in self.assentos_list.selectedItems()]
        qtd = int(self.qtd_ingressos.text() or 0)
        forma_pagamento = self.pagamento_combo.currentText()

        if len(assentos_selecionados) != qtd:
            QMessageBox.warning(self, "Erro", "O número de assentos selecionados deve ser igual à quantidade de ingressos!")
            return

        sucesso, mensagem = self.backend.reservar_assentos(self.sessao_id, assentos_selecionados, forma_pagamento)
        if sucesso:
            QMessageBox.information(self, "Sucesso", mensagem)
            self.accept()
        else:
            QMessageBox.critical(self, "Erro", mensagem)

class CinemaApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cinema Check-in - PobreCinema")
        self.backend = CinemaBackend()
        self.init_ui()

    def init_ui(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1a1a1a;
            }
            QLabel {
                color: #ffffff;
                font-size: 16px;
                font-family: Arial, sans-serif;
            }
            QComboBox, QLineEdit, QPushButton {
                background-color: #2a2a2a;
                color: #ffffff;
                border: 1px solid #444;
                border-radius: 8px;
                padding: 8px;
                font-size: 14px;
            }
            QPushButton {
                background-color: #e50914;
            }
            QPushButton:hover {
                background-color: #f40612;
            }
            QListWidget {
                background-color: #2a2a2a;
                color: #ffffff;
                border: 1px solid #444;
                border-radius: 8px;
            }
        """)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)

        # Barra de Navegação
        nav_bar = QHBoxLayout()
        nav_labels = ["Início", "Filmes", "Sessões", "Reservas"]
        for label_text in nav_labels:
            nav_label = QLabel(label_text)
            nav_label.setStyleSheet("padding: 10px; font-size: 18px; color: #b3b3b3;")
            nav_label.mousePressEvent = lambda e, t=label_text: self.nav_click(t)
            nav_bar.addWidget(nav_label)
        self.main_layout.addLayout(nav_bar)

        # Título
        title = QLabel("PobreCinema")
        title.setStyleSheet("font-size: 32px; color: #e50914; font-weight: bold; padding: 10px;")
        self.main_layout.addWidget(title)

        # Seções de Conteúdo (Scroll Area)
        scroll = QScrollArea()
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll.setWidget(scroll_content)
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("background-color: transparent; border: none;")

        # Seção 1: Filmes em Cartaz
        filmes_section = self.create_section("Filmes em Cartaz")
        grid_filmes = QGridLayout()
        filmes = self.backend.get_filmes_all()
        for idx, filme in enumerate(filmes):
            poster = PosterWidget(self.backend, filme[0], self)
            poster.setStyleSheet("""
                background-color: #333;
                border-radius: 8px;
                padding: 10px;
                min-width: 150px;
                min-height: 200px;
                qproperty-alignment: AlignCenter;
            """)
            grid_filmes.addWidget(poster, idx // 4, idx % 4)
        filmes_section.layout().addLayout(grid_filmes)
        scroll_layout.addWidget(filmes_section)

        self.main_layout.addWidget(scroll)

    def create_section(self, title):
        section = QWidget()
        layout = QVBoxLayout(section)
        title_label = QLabel(title)
        title_label.setStyleSheet("font-size: 20px; color: #ffffff; padding: 10px;")
        layout.addWidget(title_label)
        return section

    def nav_click(self, text):
        print(f"Navegação para: {text}")

class PosterWidget(QLabel):
    def __init__(self, backend, filme_id, parent=None):
        super().__init__(parent)
        self.backend = backend
        self.filme_id = filme_id
        self.setText(f"Poster: {self.filme_id}")
        self.setAlignment(Qt.AlignCenter)
        self.mousePressEvent = self.on_click

    def on_click(self, event):
        info_window = FilmeInfoWindow(self.backend, self.filme_id, self.parent())
        info_window.exec()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CinemaApp()
    window.resize(800, 600)
    window.show()
    sys.exit(app.exec())