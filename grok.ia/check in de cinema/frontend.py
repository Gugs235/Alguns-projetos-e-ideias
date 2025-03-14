# frontend.py
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QMessageBox, QScrollArea, QGridLayout, QDialog, QComboBox, QListWidget, QTextEdit
from PySide6.QtCore import Qt, QSize
from backend import CinemaBackend
import sys

class LoginWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.backend = CinemaBackend()
        self.app_parent = parent  # Referência ao CinemaApp
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        # Logo e Nome da Empresa
        logo = QLabel("🎬 PobreCinema")
        logo.setStyleSheet("font-size: 40px; color: #e50914; font-weight: bold; padding: 20px;")
        layout.addWidget(logo)

        # Cards com Imagens de Filmes
        cards_layout = QHBoxLayout()
        for i in range(3):
            card = QLabel(f"Filme {i+1}")
            card.setStyleSheet("""
                background-color: #333;
                border-radius: 8px;
                padding: 10px;
                min-width: 150px;
                min-height: 200px;
                qproperty-alignment: AlignCenter;
            """)
            cards_layout.addWidget(card)
        layout.addLayout(cards_layout)

        # Texto de Boas-Vindas
        welcome_text = QLabel("Bem-vindo ao PobreCinema! Faça login ou cadastre-se para comprar ingressos.")
        welcome_text.setStyleSheet("font-size: 16px; color: #ffffff; padding: 10px;")
        layout.addWidget(welcome_text)

        # Botões de Login e Cadastro
        login_btn = QPushButton("Login")
        login_btn.clicked.connect(self.show_login_form)
        login_btn.setStyleSheet("background-color: #e50914; color: #ffffff; padding: 10px; border-radius: 8px;")
        layout.addWidget(login_btn)

        cadastro_btn = QPushButton("Cadastrar")
        cadastro_btn.clicked.connect(self.show_cadastro_form)
        cadastro_btn.setStyleSheet("background-color: #e50914; color: #ffffff; padding: 10px; border-radius: 8px;")
        layout.addWidget(cadastro_btn)

        self.setStyleSheet("background-color: #1a1a1a;")

    def show_login_form(self):
        self.login_form = LoginForm(self.app_parent, self)  # Passa app_parent (CinemaApp)
        self.login_form.show()

    def show_cadastro_form(self):
        self.cadastro_form = CadastroForm(self.app_parent, self)  # Passa app_parent (CinemaApp)
        self.cadastro_form.show()

class LoginForm(QDialog):
    def __init__(self, app_parent=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Login")
        self.backend = CinemaBackend()
        self.app_parent = app_parent  # Referência ao CinemaApp
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        self.nome_input = QLineEdit()
        self.nome_input.setPlaceholderText("Nome")
        layout.addWidget(self.nome_input)

        self.senha_input = QLineEdit()
        self.senha_input.setPlaceholderText("Senha")
        self.senha_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.senha_input)

        login_btn = QPushButton("Entrar")
        login_btn.clicked.connect(self.fazer_login)
        layout.addWidget(login_btn)

        self.setStyleSheet("""
            QDialog {
                background-color: #1a1a1a;
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
        """)
        self.setFixedSize(300, 200)

    def fazer_login(self):
        nome = self.nome_input.text()
        senha = self.senha_input.text()
        sucesso, usuario_id, usuario_nome = self.backend.login(nome, senha)
        if sucesso:
            self.app_parent.show_main_window(usuario_id, usuario_nome)  # Usa app_parent diretamente
            self.accept()
        else:
            QMessageBox.critical(self, "Erro", "Nome ou senha incorretos!")

class CadastroForm(QDialog):
    def __init__(self, app_parent=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Cadastro")
        self.backend = CinemaBackend()
        self.app_parent = app_parent  # Referência ao CinemaApp
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        self.nome_input = QLineEdit()
        self.nome_input.setPlaceholderText("Nome")
        layout.addWidget(self.nome_input)

        self.sobrenome_input = QLineEdit()
        self.sobrenome_input.setPlaceholderText("Sobrenome")
        layout.addWidget(self.sobrenome_input)

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("E-mail")
        layout.addWidget(self.email_input)

        self.senha_input = QLineEdit()
        self.senha_input.setPlaceholderText("Senha")
        self.senha_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.senha_input)

        self.conf_senha_input = QLineEdit()
        self.conf_senha_input.setPlaceholderText("Confirmar Senha")
        self.conf_senha_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.conf_senha_input)

        cadastrar_btn = QPushButton("Cadastrar")
        cadastrar_btn.clicked.connect(self.fazer_cadastro)
        layout.addWidget(cadastrar_btn)

        self.setStyleSheet("""
            QDialog {
                background-color: #1a1a1a;
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
        """)
        self.setFixedSize(300, 300)

    def fazer_cadastro(self):
        nome = self.nome_input.text()
        sobrenome = self.sobrenome_input.text()
        email = self.email_input.text()
        senha = self.senha_input.text()
        conf_senha = self.conf_senha_input.text()

        if senha != conf_senha:
            QMessageBox.critical(self, "Erro", "As senhas não coincidem!")
            return

        sucesso, mensagem = self.backend.cadastrar_usuario(nome, sobrenome, email, senha)
        if sucesso:
            QMessageBox.information(self, "Sucesso", mensagem)
            self.accept()
        else:
            QMessageBox.critical(self, "Erro", mensagem)

class FilmeInfoWindow(QDialog):
    def __init__(self, backend, usuario_id, filme_id, parent=None):
        super().__init__(parent)
        self.backend = backend
        self.usuario_id = usuario_id
        self.filme_id = filme_id
        self.setWindowTitle("Informações do Filme")
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(10)  # Adiciona espaçamento entre os widgets
        layout.setContentsMargins(10, 10, 10, 10)  # Margens ao redor do layout

        # Título do filme
        filme_info = self.backend.get_filme_info(self.filme_id)
        title_label = QLabel(filme_info[1])
        title_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #ffffff; padding: 5px;")
        layout.addWidget(title_label)

        # Informações do filme
        info_layout = QVBoxLayout()
        info_layout.addWidget(QLabel(f"Duração: {filme_info[3]}"))
        info_layout.addWidget(QLabel(f"Data de Lançamento: {filme_info[4]}"))
        info_layout.addWidget(QLabel(f"Gênero: {filme_info[5]}"))
        info_layout.addWidget(QLabel(f"Classificação: {filme_info[6]}"))

        # Sinopse com QTextEdit ajustável
        sinopse_widget = QWidget()
        sinopse_layout = QVBoxLayout(sinopse_widget)
        sinopse_label = QLabel("Sinopse:")
        sinopse_label.setStyleSheet("color: #ffffff; font-size: 16px; font-weight: bold;")
        sinopse_text = QTextEdit(filme_info[7])
        sinopse_text.setReadOnly(True)
        sinopse_text.setFixedHeight(100)  # Limita a altura para evitar que domine
        sinopse_text.setStyleSheet("background-color: #2a2a2a; color: #ffffff; border: 1px solid #444; border-radius: 5px; padding: 5px;")
        sinopse_layout.addWidget(sinopse_label)
        sinopse_layout.addWidget(sinopse_text)
        info_layout.addWidget(sinopse_widget)

        # Trailer
        trailer_label = QLabel(f"Trailer: {filme_info[8]}")
        trailer_label.setStyleSheet("color: #ffffff; font-size: 16px;")
        info_layout.addWidget(trailer_label)

        layout.addLayout(info_layout)

        # Botões
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)  # Espaçamento entre botões
        favoritar_btn = QPushButton("Favoritar")
        favoritar_btn.clicked.connect(self.favoritar_filme)
        favoritar_btn.setStyleSheet("background-color: #e50914; color: #ffffff; border-radius: 8px; padding: 8px;")
        button_layout.addWidget(favoritar_btn)

        comprar_btn = QPushButton("Comprar Ingresso")
        comprar_btn.clicked.connect(self.abrir_selecao_sessao)
        comprar_btn.setStyleSheet("background-color: #e50914; color: #ffffff; border-radius: 8px; padding: 8px;")
        button_layout.addWidget(comprar_btn)

        layout.addLayout(button_layout)

        self.setStyleSheet("""
            QDialog {
                background-color: #1a1a1a;
            }
            QLabel {
                color: #ffffff;
                font-size: 16px;
            }
            QPushButton {
                min-width: 120px;
            }
        """)
        self.setMinimumSize(400, 500)  # Tamanho mínimo em vez de fixo
        self.adjustSize()  # Ajusta o tamanho automaticamente ao conteúdo

    def favoritar_filme(self):
        self.backend.adicionar_favorito(self.usuario_id, self.filme_id)
        QMessageBox.information(self, "Sucesso", "Filme adicionado aos favoritos!")

    def abrir_selecao_sessao(self):
        self.sessao_window = SessaoWindow(self.backend, self.usuario_id, self.filme_id, self)
        self.sessao_window.exec()

class SessaoWindow(QDialog):
    def __init__(self, backend, usuario_id, filme_id, parent=None):
        super().__init__(parent)
        self.backend = backend
        self.usuario_id = usuario_id
        self.filme_id = filme_id
        self.setWindowTitle("Seleção de Sessão")
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        self.sessao_list = QListWidget()
        sessoes_info = self.backend.get_sessoes_info(self.filme_id)
        for sessao in sessoes_info:
            sessao_id, data, horario, tipo_sala, cinema_nome = sessao
            self.sessao_list.addItem(f"{sessao_id} - {cinema_nome} - {data} às {horario} ({tipo_sala})")
        self.sessao_list.itemClicked.connect(self.on_sessao_selected)
        layout.addWidget(QLabel("Sessões Disponíveis:"))
        layout.addWidget(self.sessao_list)

        self.assentos_grid = QGridLayout()
        self.assentos = {}
        layout.addWidget(QLabel("Mapa de Assentos:"))
        layout.addLayout(self.assentos_grid)

        self.confirmar_btn = QPushButton("Confirmar")
        self.confirmar_btn.clicked.connect(self.abrir_compra)
        self.confirmar_btn.setEnabled(False)
        layout.addWidget(self.confirmar_btn)

        self.setStyleSheet("""
            QDialog {
                background-color: #1a1a1a;
            }
            QLabel {
                color: #ffffff;
                font-size: 16px;
            }
            QPushButton {
                background-color: #e50914;
                color: #ffffff;
                border-radius: 8px;
                padding: 8px;
            }
            QListWidget {
                background-color: #2a2a2a;
                color: #ffffff;
                border: 1px solid #444;
                border-radius: 8px;
            }
        """)
        self.setFixedSize(500, 600)

    def on_sessao_selected(self, item):
        self.selected_sessao_id = int(item.text().split(" - ")[0])
        self.atualizar_assentos()
        self.confirmar_btn.setEnabled(True)

    def atualizar_assentos(self):
        for i in range(self.assentos_grid.count()):
            self.assentos_grid.itemAt(i).widget().deleteLater()
        self.assentos.clear()

        assentos = self.backend.get_assentos_disponiveis(self.selected_sessao_id)
        for idx, assento in enumerate(assentos[:25]):  # Mostrar 25 assentos em um grid 5x5
            btn = QPushButton(assento)
            btn.setStyleSheet("background-color: green; color: white; border-radius: 4px;")
            btn.clicked.connect(lambda checked, a=assento: self.selecionar_assento(a))
            self.assentos[assento] = btn
            self.assentos_grid.addWidget(btn, idx // 5, idx % 5)

    def selecionar_assento(self, assento):
        btn = self.assentos[assento]
        if btn.styleSheet().find("yellow") != -1:
            btn.setStyleSheet("background-color: green; color: white; border-radius: 5px;")
        else:
            btn.setStyleSheet("background-color: yellow; color: black; border-radius: 5px;")
        self.selected_assentos = [a for a, b in self.assentos.items() if b.styleSheet().find("yellow") != -1]

    def abrir_compra(self):
        if not hasattr(self, 'selected_assentos') or not self.selected_assentos:
            QMessageBox.warning(self, "Erro", "Selecione pelo menos um assento!")
            return
        self.compra_window = CompraWindow(self.backend, self.usuario_id, self.filme_id, self.selected_sessao_id, self.selected_assentos, self)
        self.compra_window.exec()

class CompraWindow(QDialog):
    def __init__(self, backend, usuario_id, filme_id, sessao_id, assentos, parent=None):
        super().__init__(parent)
        self.backend = backend
        self.usuario_id = usuario_id
        self.filme_id = filme_id
        self.sessao_id = sessao_id
        self.assentos = assentos
        self.setWindowTitle("Confirmar Compra")
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        filme_info = self.backend.get_filme_info(self.filme_id)
        sessao_info = next(s for s in self.backend.get_sessoes_info(self.filme_id) if s[0] == self.sessao_id)
        valor_por_assento = 20.0
        total = len(self.assentos) * valor_por_assento

        layout.addWidget(QLabel(f"Filme: {filme_info[1]}"))
        layout.addWidget(QLabel(f"Data e Horário: {sessao_info[1]} às {sessao_info[2]} ({sessao_info[3]})"))
        layout.addWidget(QLabel(f"Duração: {filme_info[3]}"))
        layout.addWidget(QLabel(f"Assentos Selecionados: {', '.join(self.assentos)}"))
        layout.addWidget(QLabel(f"Valor por Assento: R${valor_por_assento:.2f}"))
        layout.addWidget(QLabel(f"Total: R${total:.2f}"))

        self.pagamento_combo = QComboBox()
        self.pagamento_combo.addItems(["Cartão de Crédito/Débito", "PIX", "Boleto"])
        self.pagamento_combo.currentIndexChanged.connect(self.atualizar_forma_pagamento)
        layout.addWidget(QLabel("Forma de Pagamento:"))
        layout.addWidget(self.pagamento_combo)

        self.cartao_form = QWidget()
        cartao_layout = QVBoxLayout(self.cartao_form)
        self.nome_cartao = QLineEdit()
        self.nome_cartao.setPlaceholderText("Nome no Cartão")
        cartao_layout.addWidget(self.nome_cartao)
        self.numero_cartao = QLineEdit()
        self.numero_cartao.setPlaceholderText("Número do Cartão")
        cartao_layout.addWidget(self.numero_cartao)
        self.data_expiracao = QLineEdit()
        self.data_expiracao.setPlaceholderText("Data de Expiração (MM/AA)")
        cartao_layout.addWidget(self.data_expiracao)
        self.cvv = QLineEdit()
        self.cvv.setPlaceholderText("CVV")
        cartao_layout.addWidget(self.cvv)
        self.cartao_form.setVisible(False)
        layout.addWidget(self.cartao_form)

        pagar_btn = QPushButton("Pagar")
        pagar_btn.clicked.connect(self.confirmar_pagamento)
        layout.addWidget(pagar_btn)

        self.setStyleSheet("""
            QDialog {
                background-color: #1a1a1a;
            }
            QLabel {
                color: #ffffff;
                font-size: 16px;
            }
            QLineEdit, QComboBox, QPushButton {
                background-color: #2a2a2a;
                color: #ffffff;
                border: 1px solid #444;
                border-radius: 8px;
                padding: 8px;
            }
            QPushButton {
                background-color: #e50914;
            }
        """)
        self.setFixedSize(400, 500)

    def atualizar_forma_pagamento(self):
        self.cartao_form.setVisible(self.pagamento_combo.currentText() == "Cartão de Crédito/Débito")

    def confirmar_pagamento(self):
        forma_pagamento = self.pagamento_combo.currentText()
        if forma_pagamento == "Cartão de Crédito/Débito":
            nome_cartao = self.nome_cartao.text()
            numero_cartao = self.numero_cartao.text()
            data_expiracao = self.data_expiracao.text()
            cvv = self.cvv.text()
            if not all([nome_cartao, numero_cartao, data_expiracao, cvv]):
                QMessageBox.warning(self, "Erro", "Preencha todos os dados do cartão!")
                return
            self.backend.salvar_cartao(self.usuario_id, nome_cartao, numero_cartao, data_expiracao, cvv)

        sucesso, mensagem = self.backend.reservar_assentos(self.usuario_id, self.sessao_id, self.assentos, forma_pagamento)
        if sucesso:
            QMessageBox.information(self, "Sucesso", mensagem)
            voltar_btn = QPushButton("Voltar para a Home")
            voltar_btn.clicked.connect(self.voltar_home)
            self.layout().addWidget(voltar_btn)
        else:
            QMessageBox.critical(self, "Erro", mensagem)

    def voltar_home(self):
        self.parent().parent().parent().show_home()
        self.accept()

class CinemaApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cinema Check-in - PobreCinema")
        self.backend = CinemaBackend()
        self.init_ui()

    def init_ui(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)

        self.login_screen = LoginWindow(self)
        self.main_layout.addWidget(self.login_screen)

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
        self.resize(800, 600)

    def show_main_window(self, usuario_id, usuario_nome):
        self.main_layout.removeWidget(self.login_screen)
        self.login_screen.deleteLater()

        self.usuario_id = usuario_id
        self.usuario_nome = usuario_nome

        self.nav_bar = QHBoxLayout()
        self.nav_bar.addWidget(self.create_nav_icon("🏠", self.show_home))
        self.nav_bar.addWidget(self.create_nav_icon("⭐", self.show_favoritos))
        self.nav_bar.addWidget(self.create_nav_icon("🎟️", self.show_compras))
        self.nav_bar.addWidget(self.create_nav_icon("👤", self.show_perfil))
        self.main_layout.addLayout(self.nav_bar)

        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.main_layout.addWidget(self.content_widget)

        self.show_home()

    def create_nav_icon(self, icon, callback):
        btn = QPushButton(icon)
        btn.setStyleSheet("background-color: #2a2a2a; color: #ffffff; padding: 10px; border-radius: 8px;")
        btn.clicked.connect(callback)
        return btn

    def clear_content(self):
        for i in reversed(range(self.content_layout.count())):
            widget = self.content_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

    def show_home(self):
        self.clear_content()
        scroll = QScrollArea()
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll.setWidget(scroll_content)
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("background-color: transparent; border: none;")

        filmes_section = QWidget()
        filmes_layout = QVBoxLayout(filmes_section)
        filmes_layout.addWidget(QLabel("Filmes em Cartaz"))
        grid_filmes = QGridLayout()
        filmes = self.backend.get_filmes_all()
        for idx, filme in enumerate(filmes):
            poster = PosterWidget(self.backend, self.usuario_id, filme[0], filme[1], self)
            grid_filmes.addWidget(poster, idx // 4, idx % 4)
        filmes_layout.addLayout(grid_filmes)
        scroll_layout.addWidget(filmes_section)

        self.content_layout.addWidget(scroll)

    def show_favoritos(self):
        self.clear_content()
        scroll = QScrollArea()
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll.setWidget(scroll_content)
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("background-color: transparent; border: none;")

        favoritos_section = QWidget()
        favoritos_layout = QVBoxLayout(favoritos_section)
        favoritos_layout.addWidget(QLabel("Filmes Favoritados"))
        grid_favoritos = QGridLayout()
        favoritos = self.backend.get_favoritos(self.usuario_id)
        for idx, filme in enumerate(favoritos):
            poster = PosterWidget(self.backend, self.usuario_id, filme[0], filme[1], self)
            grid_favoritos.addWidget(poster, idx // 4, idx % 4)
        favoritos_layout.addLayout(grid_favoritos)
        scroll_layout.addWidget(favoritos_section)

        self.content_layout.addWidget(scroll)

    def show_compras(self):
        self.clear_content()
        scroll = QScrollArea()
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll.setWidget(scroll_content)
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("background-color: transparent; border: none;")

        compras_section = QWidget()
        compras_layout = QVBoxLayout(compras_section)
        compras_layout.addWidget(QLabel("Minhas Compras"))
        grid_compras = QGridLayout()
        compras = self.backend.get_compras(self.usuario_id)
        for idx, compra in enumerate(compras):
            compra_label = QLabel(f"{compra[1]} - {compra[2]} às {compra[3]} ({compra[4]}) - Assento: {compra[6]}")
            grid_compras.addWidget(compra_label, idx, 0)
        compras_layout.addLayout(grid_compras)
        scroll_layout.addWidget(compras_section)

        self.content_layout.addWidget(scroll)

    def show_perfil(self):
        self.clear_content()
        perfil_widget = QWidget()
        perfil_layout = QVBoxLayout(perfil_widget)

        usuario_info = self.backend.get_usuario_info(self.usuario_id)
        perfil_layout.addWidget(QLabel(f"Nome: {usuario_info[0]} {usuario_info[1]}"))
        perfil_layout.addWidget(QLabel(f"E-mail: {usuario_info[2]}"))
        perfil_layout.addWidget(QLabel(f"Senha: {'*' * len(usuario_info[3])}"))

        cartao_info = self.backend.get_cartao_info(self.usuario_id)
        if cartao_info:
            perfil_layout.addWidget(QLabel(f"Cartão: {'*' * 12}{cartao_info[1][-4:]}"))
            perfil_layout.addWidget(QLabel(f"Data de Expiração: {cartao_info[2]}"))

        self.content_layout.addWidget(perfil_widget)

class PosterWidget(QLabel):
    def __init__(self, backend, usuario_id, filme_id, filme_nome, parent=None):
        super().__init__(parent)
        self.backend = backend
        self.usuario_id = usuario_id
        self.filme_id = filme_id
        self.setText(f"Poster: {filme_nome}")
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet("""
            background-color: #333;
            border-radius: 8px;
            padding: 10px;
            min-width: 150px;
            min-height: 200px;
        """)
        self.mousePressEvent = self.on_click

    def on_click(self, event):
        info_window = FilmeInfoWindow(self.backend, self.usuario_id, self.filme_id, self.parent())
        info_window.exec()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CinemaApp()
    window.show()
    sys.exit(app.exec())