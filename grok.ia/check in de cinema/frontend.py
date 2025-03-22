# frontend.py
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QMessageBox, QScrollArea, QGridLayout, QDialog, QComboBox, QListWidget, QTextEdit, QCheckBox
from PySide6.QtCore import Qt, QSize, QUrl
from backend import CinemaBackend
import sys
import os
from PySide6.QtMultimedia import QMediaPlayer
from PySide6.QtMultimediaWidgets import QVideoWidget
import yt_dlp
from PyQt6.QtGui import QPixmap  # Adicionando QPixmap para trabalhar com imagens
from PySide6.QtGui import QPixmap  # Importar QPixmap do PySide6
import requests
from PySide6.QtCore import QByteArray
from PySide6.QtGui import QPixmap

class LoginWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.backend = CinemaBackend()
        self.app_parent = parent  # Referência ao CinemaApp
        self.login_form = None  # Referência para a instância de LoginForm
        self.cadastro_form = None  # Referência para a instância de CadastroForm
        self.login_btn = None  # Referência para o botão de login
        self.cadastro_btn = None  # Referência para o botão de cadastro
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
        self.login_btn = QPushButton("Login")
        self.login_btn.clicked.connect(self.show_login_form)
        self.login_btn.setStyleSheet("background-color: #e50914; color: #ffffff; padding: 10px; border-radius: 8px;")
        layout.addWidget(self.login_btn)

        self.cadastro_btn = QPushButton("Cadastrar")
        self.cadastro_btn.clicked.connect(self.show_cadastro_form)
        self.cadastro_btn.setStyleSheet("background-color: #e50914; color: #ffffff; padding: 10px; border-radius: 8px;")
        layout.addWidget(self.cadastro_btn)

        self.setStyleSheet("background-color: #1a1a1a;")

    def show_login_form(self):
        # Desabilitar os botões para evitar múltiplos cliques
        self.login_btn.setEnabled(False)
        self.cadastro_btn.setEnabled(False)

        # Fechar o formulário de cadastro, se estiver aberto
        if self.cadastro_form and self.cadastro_form.isVisible():
            self.cadastro_form.close()

        # Fechar o formulário de login existente, se estiver aberto
        if self.login_form and self.login_form.isVisible():
            self.login_form.close()

        # Criar e exibir o novo formulário de login
        self.login_form = LoginForm(self.backend, self.app_parent, self)
        self.login_form.show()

        # Reabilitar os botões quando o formulário for fechado
        self.login_form.finished.connect(lambda: self.enable_buttons())

    def show_cadastro_form(self):
        # Desabilitar os botões para evitar múltiplos cliques
        self.login_btn.setEnabled(False)
        self.cadastro_btn.setEnabled(False)

        # Fechar o formulário de login, se estiver aberto
        if self.login_form and self.login_form.isVisible():
            self.login_form.close()

        # Fechar o formulário de cadastro existente, se estiver aberto
        if self.cadastro_form and self.cadastro_form.isVisible():
            self.cadastro_form.close()

        # Criar e exibir o novo formulário de cadastro
        self.cadastro_form = CadastroForm(self.backend, self.app_parent, self)
        self.cadastro_form.show()

        # Reabilitar os botões quando o formulário for fechado
        self.cadastro_form.finished.connect(lambda: self.enable_buttons())

    def enable_buttons(self):
        # Reabilitar os botões
        self.login_btn.setEnabled(True)
        self.cadastro_btn.setEnabled(True)

class LoginForm(QDialog):
    def __init__(self, backend, app_parent, parent=None):
        super().__init__(parent)
        self.backend = backend  # Recebe o backend como parâmetro
        self.app_parent = app_parent
        self.setWindowTitle("Login")
        self.setGeometry(300, 300, 300, 300)
        self.setStyleSheet("background-color: #1a1a1a;")
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Título
        title = QLabel("Login")
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: #ffffff;")
        layout.addWidget(title)

        # Campo Email
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email")
        self.email_input.setStyleSheet("background-color: #333333; color: #ffffff; padding: 5px;")
        layout.addWidget(self.email_input)

        # Campo Senha
        self.senha_input = QLineEdit()
        self.senha_input.setPlaceholderText("Senha")
        self.senha_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.senha_input.setStyleSheet("background-color: #333333; color: #ffffff; padding: 5px;")
        layout.addWidget(self.senha_input)

        # Botão Login
        login_btn = QPushButton("Entrar")
        login_btn.setStyleSheet("background-color: #e50914; color: #ffffff; padding: 10px; border-radius: 8px;")
        login_btn.clicked.connect(self.login)
        layout.addWidget(login_btn)

        # Botão Voltar
        voltar_btn = QPushButton("Voltar")
        voltar_btn.setStyleSheet("background-color: #555555; color: #ffffff; padding: 10px; border-radius: 8px;")
        voltar_btn.clicked.connect(self.close)
        layout.addWidget(voltar_btn)

        self.setLayout(layout)

    def login(self):
        email = self.email_input.text().strip()
        senha = self.senha_input.text().strip()

        # Validação dos campos
        if not email:
            QMessageBox.warning(self, "Erro", "O campo Email é obrigatório!")
            return
        if not senha:
            QMessageBox.warning(self, "Erro", "O campo Senha é obrigatório!")
            return

        # Tentar fazer login
        usuario = self.backend.login_usuario(email, senha)
        if usuario:
            usuario_id, nome = usuario
            QMessageBox.information(self, "Sucesso", f"Bem-vindo, {nome}!")
            self.close()
            self.app_parent.show_main_window(usuario_id, nome)
        else:
            QMessageBox.warning(self, "Erro", "Email ou senha incorretos!")

class CadastroForm(QDialog):
    def __init__(self, backend, app_parent, parent=None):
        super().__init__(parent)
        self.backend = backend  # Recebe o backend como parâmetro
        self.app_parent = app_parent
        self.setWindowTitle("Cadastro")
        self.setGeometry(300, 300, 300, 400)
        self.setStyleSheet("background-color: #1a1a1a;")
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Título
        title = QLabel("Criar Conta")
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: #ffffff;")
        layout.addWidget(title)

        # Campo Nome
        self.nome_input = QLineEdit()
        self.nome_input.setPlaceholderText("Nome")
        self.nome_input.setStyleSheet("background-color: #333333; color: #ffffff; padding: 5px;")
        layout.addWidget(self.nome_input)

        # Campo Sobrenome
        self.sobrenome_input = QLineEdit()
        self.sobrenome_input.setPlaceholderText("Sobrenome")
        self.sobrenome_input.setStyleSheet("background-color: #333333; color: #ffffff; padding: 5px;")
        layout.addWidget(self.sobrenome_input)

        # Campo Email
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email")
        self.email_input.setStyleSheet("background-color: #333333; color: #ffffff; padding: 5px;")
        layout.addWidget(self.email_input)

        # Campo Senha
        self.senha_input = QLineEdit()
        self.senha_input.setPlaceholderText("Senha")
        self.senha_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.senha_input.setStyleSheet("background-color: #333333; color: #ffffff; padding: 5px;")
        layout.addWidget(self.senha_input)

        # Botão Cadastrar
        cadastrar_btn = QPushButton("Cadastrar")
        cadastrar_btn.setStyleSheet("background-color: #e50914; color: #ffffff; padding: 10px; border-radius: 8px;")
        cadastrar_btn.clicked.connect(self.cadastrar)
        layout.addWidget(cadastrar_btn)

        # Botão Voltar
        voltar_btn = QPushButton("Voltar")
        voltar_btn.setStyleSheet("background-color: #555555; color: #ffffff; padding: 10px; border-radius: 8px;")
        voltar_btn.clicked.connect(self.close)
        layout.addWidget(voltar_btn)

        self.setLayout(layout)

    def cadastrar(self):
        nome = self.nome_input.text().strip()
        sobrenome = self.sobrenome_input.text().strip()
        email = self.email_input.text().strip()
        senha = self.senha_input.text().strip()

        # Validação dos campos
        if not nome:
            QMessageBox.warning(self, "Erro", "O campo Nome é obrigatório!")
            return
        if not sobrenome:
            QMessageBox.warning(self, "Erro", "O campo Sobrenome é obrigatório!")
            return
        if not email:
            QMessageBox.warning(self, "Erro", "O campo Email é obrigatório!")
            return
        if not senha:
            QMessageBox.warning(self, "Erro", "O campo Senha é obrigatório!")
            return

        # Tentar cadastrar o usuário
        try:
            usuario_id = self.backend.cadastrar_usuario(nome, sobrenome, email, senha)
            if usuario_id:
                QMessageBox.information(self, "Sucesso", "Usuário cadastrado com sucesso!")
                self.close()
                self.app_parent.show_main_window(usuario_id, nome)
            else:
                QMessageBox.warning(self, "Erro", "Erro ao cadastrar usuário. Verifique os dados e tente novamente.")
        except Exception as e:
            QMessageBox.warning(self, "Erro", f"Erro ao cadastrar: {str(e)}")

from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QMessageBox
from PySide6.QtCore import Qt

class FilmeInfoWindow(QDialog):
    def __init__(self, filme_id, filme_nome, backend, usuario_id, parent=None):
        super().__init__(parent=parent)  # Inicializar o QDialog com o parent
        self.filme_id = filme_id
        self.filme_nome = filme_nome
        self.backend = backend
        self.usuario_id = usuario_id  # Armazenar o usuario_id
        self.parent = parent
        self.setWindowTitle(f"Informações do Filme: {filme_nome}")
        self.setGeometry(300, 300, 400, 500)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        # Obter informações do filme
        filme_info = self.backend.get_filme_info(self.filme_id)
        if filme_info:
            nome = filme_info[1]
            cinema_id = filme_info[2]
            duracao = filme_info[3]
            data_lancamento = filme_info[4]
            genero = filme_info[5]
            classificacao = filme_info[6]
            sinopse = filme_info[7]
            trailer_url = filme_info[8]

            # Exibir informações do filme
            layout.addWidget(QLabel(f"<h2>{nome}</h2>"))
            layout.addWidget(QLabel(f"<b>Gênero:</b> {genero}"))
            layout.addWidget(QLabel(f"<b>Duração:</b> {duracao}"))
            layout.addWidget(QLabel(f"<b>Classificação:</b> {classificacao}"))
            layout.addWidget(QLabel(f"<b>Data de Lançamento:</b> {data_lancamento}"))
            layout.addWidget(QLabel(f"<b>Sinopse:</b> {sinopse}"))

            # Link do trailer
            trailer_label = QLabel(f'<a href="{trailer_url}">Assistir Trailer</a>')
            trailer_label.setTextInteractionFlags(Qt.TextBrowserInteraction)
            trailer_label.setOpenExternalLinks(True)
            layout.addWidget(trailer_label)

        else:
            layout.addWidget(QLabel("Erro: Não foi possível carregar as informações do filme."))

        # Botão de Favoritar
        favoritar_btn = QPushButton("Favoritar")
        favoritar_btn.clicked.connect(self.favoritar_filme)
        layout.addWidget(favoritar_btn)

        # Botão de Comprar Ingresso
        comprar_btn = QPushButton("Comprar Ingresso")
        comprar_btn.clicked.connect(self.abrir_sessoes)
        layout.addWidget(comprar_btn)

        # Botão de Fechar
        fechar_btn = QPushButton("Fechar")
        fechar_btn.clicked.connect(self.close)
        layout.addWidget(fechar_btn)

    def favoritar_filme(self):
        """Adiciona o filme aos favoritos."""
        try:
            self.backend.adicionar_favorito(self.filme_id)
            QMessageBox.information(self, "Sucesso", f"{self.filme_nome} foi adicionado aos favoritos!")
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao favoritar o filme: {str(e)}")

    def abrir_sessoes(self):
        """Abre a tela de escolha de sessões e assentos."""
        self.sessoes_window = SessaoWindow(self.backend, self.usuario_id, self.filme_id, self.parent, self)
        self.sessoes_window.show()
        self.close()  # Fecha a janela de informações do filme

class SessaoWindow(QDialog):
    def __init__(self, backend, usuario_id, filme_id, app_parent, parent=None):
        super().__init__(parent)
        self.backend = backend
        self.usuario_id = usuario_id
        self.filme_id = filme_id
        self.app_parent = app_parent
        self.parent = parent
        self.selected_assentos = []  # Lista para armazenar os assentos selecionados
        self.assentos = {}  # Dicionário para armazenar os botões de assento
        self.setStyleSheet("background-color: #1a1a1a;")
        self.init_ui()

    def init_ui(self):
            self.setWindowTitle("Selecionar Sessão e Assentos")
            self.setGeometry(300, 300, 600, 600)
            layout = QVBoxLayout()

            # Título
            title_label = QLabel("Selecione uma Sessão e os Assentos", self)
            title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            title_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #ffffff;")
            layout.addWidget(title_label)

            # Lista de sessões
            self.sessao_combo = QComboBox(self)
            self.sessao_combo.setStyleSheet("background-color: #333333; color: #ffffff; padding: 5px;")
            sessoes = self.backend.get_sessoes_info(self.filme_id)
            for sessao in sessoes:
                sessao_id, data, horario, tipo_sala, cinema_nome = sessao
                self.sessao_combo.addItem(f"{cinema_nome} - {data} {horario} ({tipo_sala})", sessao_id)
            self.sessao_combo.currentIndexChanged.connect(self.atualizar_assentos)
            layout.addWidget(self.sessao_combo)

            # Área de assentos
            self.assentos_widget = QWidget()
            self.assentos_grid = QGridLayout(self.assentos_widget)
            layout.addWidget(self.assentos_widget)

            # Botões
            btn_layout = QHBoxLayout()
            self.btn_confirmar = QPushButton("Confirmar", self)
            self.btn_confirmar.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px; border-radius: 5px;")
            self.btn_confirmar.clicked.connect(self.confirmar_sessao)
            self.btn_confirmar.setEnabled(False)  # Desabilitado até selecionar assentos
            btn_layout.addWidget(self.btn_confirmar)

            btn_voltar = QPushButton("Voltar", self)
            btn_voltar.setStyleSheet("background-color: #f44336; color: white; padding: 10px; border-radius: 5px;")
            btn_voltar.clicked.connect(self.voltar)
            btn_layout.addWidget(btn_voltar)

            layout.addLayout(btn_layout)
            self.setLayout(layout)

            # Atualizar assentos para a primeira sessão, se houver
            if self.sessao_combo.count() > 0:
                self.atualizar_assentos()

    def on_sessao_selected(self, item):
        self.selected_sessao_id = int(item.text().split(" - ")[0])
        self.atualizar_assentos()
        self.confirmar_btn.setEnabled(True)

    def abrir_compra(self):
        if not hasattr(self, 'selected_assentos') or not self.selected_assentos:
            QMessageBox.warning(self, "Erro", "Selecione pelo menos um assento!")
            return
        # Passa self.app_parent (CinemaApp) como app_parent para CompraWindow
        self.compra_window = CompraWindow(self.backend, self.usuario_id, self.filme_id, self.selected_sessao_id, self.selected_assentos, self.app_parent, self)
        self.compra_window.exec()

    def atualizar_assentos(self):
            # Limpar assentos anteriores
            for i in reversed(range(self.assentos_grid.count())):
                widget = self.assentos_grid.itemAt(i).widget()
                if widget:
                    widget.deleteLater()
            self.assentos.clear()
            self.selected_assentos.clear()
            self.btn_confirmar.setEnabled(False)

            # Obter assentos disponíveis para a sessão selecionada
            sessao_id = self.sessao_combo.currentData()
            if not sessao_id:
                return

            self.selected_sessao_id = sessao_id
            assentos_disponiveis = self.backend.get_assentos_disponiveis(sessao_id)
            _, maxima = self.backend.get_lotacao_atual(sessao_id)
            assentos_exibir = [f"A{i:02d}" for i in range(1, min(26, maxima + 1))]  # Limita ao mínimo de 25 ou lotação máxima

            for idx, assento in enumerate(assentos_exibir):
                btn = QPushButton(assento)
                btn.setStyleSheet("""
                    background-color: green;
                    color: white;
                    border-radius: 5px;
                    min-width: 50px;
                    min-height: 50px;
                    width: 50px;
                    height: 50px;
                    font-size: 14px;
                """)
                btn.clicked.connect(lambda checked, a=assento: self.selecionar_assento(a))
                if assento not in assentos_disponiveis:
                    btn.setStyleSheet("""
                        background-color: gray;
                        color: white;
                        border-radius: 5px;
                        min-width: 50px;
                        min-height: 50px;
                        width: 50px;
                        height: 50px;
                        font-size: 14px;
                    """)
                    btn.setEnabled(False)
                self.assentos[assento] = btn
                self.assentos_grid.addWidget(btn, idx // 5, idx % 5)

            self.assentos_grid.setSpacing(10)

    def selecionar_assento(self, assento):
            btn = self.assentos[assento]
            is_selected = "yellow" in btn.styleSheet()
            if is_selected:
                btn.setStyleSheet("""
                    background-color: green;
                    color: white;
                    border-radius: 5px;
                    min-width: 50px;
                    min-height: 50px;
                    width: 50px;
                    height: 50px;
                    font-size: 14px;
                """)
                if assento in self.selected_assentos:
                    self.selected_assentos.remove(assento)
            else:
                if assento not in self.selected_assentos and len(self.selected_assentos) < 10:
                    btn.setStyleSheet("""
                        background-color: yellow;
                        color: black;
                        border-radius: 5px;
                        min-width: 50px;
                        min-height: 50px;
                        width: 50px;
                        height: 50px;
                        font-size: 14px;
                    """)
                    self.selected_assentos.append(assento)
                else:
                    QMessageBox.warning(self, "Erro", "Assento já selecionado ou limite de 10 assentos atingido!")
                    return

            # Habilitar o botão de confirmar se houver assentos selecionados
            self.btn_confirmar.setEnabled(len(self.selected_assentos) > 0)

    def confirmar_sessao(self):
        if not self.selected_assentos:
            QMessageBox.warning(self, "Erro", "Selecione pelo menos um assento!")
            return

        sessao_id = self.sessao_combo.currentData()
        if sessao_id:
            self.compra_window = CompraWindow(self.backend, self.usuario_id, self.filme_id, sessao_id, self.selected_assentos, self.app_parent, self)
            self.compra_window.show()
            self.hide()
        else:
            QMessageBox.warning(self, "Erro", "Selecione uma sessão válida!")

    def voltar(self):
        self.hide()
        if self.parent:
            self.parent.show()

    def abrir_compra(self):
        if not hasattr(self, 'selected_assentos') or not self.selected_assentos:
            QMessageBox.warning(self, "Erro", "Selecione pelo menos um assento!")
            return
        self.compra_window = CompraWindow(self.backend, self.usuario_id, self.filme_id, self.selected_sessao_id, self.selected_assentos, self)
        self.compra_window.exec()

class CompraWindow(QDialog):
    def __init__(self, backend, usuario_id, filme_id, sessao_id, assentos, app_parent, parent=None):
        super().__init__(parent)
        self.backend = backend
        self.usuario_id = usuario_id
        self.filme_id = filme_id
        self.sessao_id = sessao_id
        self.assentos = assentos
        self.app_parent = app_parent
        self.cartao_info = None
        self.voltar_btn = None
        self.pix_confirmado = False
        self.boleto_confirmado = False
        self.pagar_btn = None  # Referência ao botão "Pagar"
        self.setWindowTitle("Confirmar Compra")
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout(self)

        filme_info = self.backend.get_filme_info(self.filme_id)
        sessao_info = next(s for s in self.backend.get_sessoes_info(self.filme_id) if s[0] == self.sessao_id)
        valor_por_assento = 20.0
        self.total = len(self.assentos) * valor_por_assento

        self.layout.addWidget(QLabel(f"Filme: {filme_info[1]}"))
        self.layout.addWidget(QLabel(f"Data e Horário: {sessao_info[1]} às {sessao_info[2]} ({sessao_info[3]})"))
        self.layout.addWidget(QLabel(f"Duração: {filme_info[3]}"))
        self.layout.addWidget(QLabel(f"Assentos Selecionados: {', '.join(self.assentos)}"))
        self.layout.addWidget(QLabel(f"Valor por Assento: R${valor_por_assento:.2f}"))
        self.layout.addWidget(QLabel(f"Total: R${self.total:.2f}"))

        self.layout.addWidget(QLabel("Forma de Pagamento:"))
        self.pagamento_combo = QComboBox()
        self.pagamento_combo.addItems(["Cartão de Crédito/Débito", "PIX", "Boleto"])
        self.pagamento_combo.currentIndexChanged.connect(self.atualizar_forma_pagamento)
        self.layout.addWidget(self.pagamento_combo)

        # Widget para exibir informações do cartão
        self.cartao_widget = QWidget()
        self.cartao_layout = QVBoxLayout(self.cartao_widget)
        self.cartao_label = QLabel("Nenhum cartão cadastrado.")
        self.cartao_label.setStyleSheet("color: #ffffff; font-size: 14px;")
        self.cartao_layout.addWidget(self.cartao_label)

        self.cartao_btn = QPushButton("Adicionar/Alterar Cartão")
        self.cartao_btn.setStyleSheet("background-color: #e50914; color: #ffffff; padding: 8px; border-radius: 8px;")
        self.cartao_btn.clicked.connect(self.abrir_cartao_window)
        self.cartao_layout.addWidget(self.cartao_btn)
        self.cartao_widget.setVisible(False)
        self.layout.addWidget(self.cartao_widget)

        # Widget para exibir botão de PIX
        self.pix_widget = QWidget()
        self.pix_layout = QVBoxLayout(self.pix_widget)
        self.pix_btn = QPushButton("Gerar PIX")
        self.pix_btn.setStyleSheet("background-color: #e50914; color: #ffffff; padding: 8px; border-radius: 8px;")
        self.pix_btn.clicked.connect(self.abrir_pix_window)
        self.pix_layout.addWidget(self.pix_btn)
        self.pix_widget.setVisible(False)
        self.layout.addWidget(self.pix_widget)

        # Widget para exibir botão de Boleto
        self.boleto_widget = QWidget()
        self.boleto_layout = QVBoxLayout(self.boleto_widget)
        self.boleto_btn = QPushButton("Gerar Boleto")
        self.boleto_btn.setStyleSheet("background-color: #e50914; color: #ffffff; padding: 8px; border-radius: 8px;")
        self.boleto_btn.clicked.connect(self.abrir_boleto_window)
        self.boleto_layout.addWidget(self.boleto_btn)
        self.boleto_widget.setVisible(False)
        self.layout.addWidget(self.boleto_widget)

        # Botão Pagar (inicialmente desabilitado para PIX e Boleto)
        self.pagar_btn = QPushButton("Pagar")
        self.pagar_btn.clicked.connect(self.confirmar_pagamento)
        self.pagar_btn.setStyleSheet("""
            QPushButton {
                background-color: #e50914;
                color: #ffffff;
                border: 1px solid #444;
                border-radius: 8px;
                padding: 8px;
            }
            QPushButton:disabled {
                background-color: #a34045;
                opacity: 80;  /* Torna o botão opaco quando desabilitado */
                color: #808080;  /* Cor do texto mais clara para indicar desabilitado */
            }
        """)
        self.layout.addWidget(self.pagar_btn)

        self.setStyleSheet("""
            QDialog {
                background-color: #1a1a1a;
            }
            QLabel {
                color: #ffffff;
                font-size: 16px;
            }
            QLineEdit, QComboBox {
                background-color: #2a2a2a;
                color: #ffffff;
                border: 1px solid #444;
                border-radius: 8px;
                padding: 8px;
            }
        """)
        self.setFixedSize(400, 500)

        # Verificar se já existe um cartão cadastrado e ajustar o estado do botão "Pagar"
        self.atualizar_forma_pagamento()

    def atualizar_forma_pagamento(self):
        forma_pagamento = self.pagamento_combo.currentText()
        self.cartao_widget.setVisible(forma_pagamento == "Cartão de Crédito/Débito")
        self.pix_widget.setVisible(forma_pagamento == "PIX")
        self.boleto_widget.setVisible(forma_pagamento == "Boleto")

        if forma_pagamento == "Cartão de Crédito/Débito":
            self.cartao_info = self.backend.get_cartao_info(self.usuario_id)
            if self.cartao_info:
                self.cartao_label.setText(f"Cartão: **** **** **** {self.cartao_info[1][-4:]} (Exp.: {self.cartao_info[2]})")
                self.pagar_btn.setEnabled(True)  # Habilitar o botão "Pagar" se houver cartão
            else:
                self.cartao_label.setText("Nenhum cartão cadastrado.")
                self.pagar_btn.setEnabled(False)  # Desabilitar até que o cartão seja cadastrado
        elif forma_pagamento == "PIX":
            self.pix_confirmado = False
            self.pagar_btn.setEnabled(False)  # Desabilitar até que o PIX seja gerado
        elif forma_pagamento == "Boleto":
            self.boleto_confirmado = False
            self.pagar_btn.setEnabled(False)  # Desabilitar até que o boleto seja gerado

    def abrir_cartao_window(self):
        cartao_window = CartaoWindow(self.backend, self.usuario_id, self)
        if cartao_window.exec() == QDialog.Accepted:
            # Atualizar as informações do cartão após o cadastro
            self.cartao_info = self.backend.get_cartao_info(self.usuario_id)
            if self.cartao_info:
                self.cartao_label.setText(f"Cartão: **** **** **** {self.cartao_info[1][-4:]} (Exp.: {self.cartao_info[2]})")
                self.pagar_btn.setEnabled(True)  # Habilitar o botão "Pagar" após cadastrar o cartão
            else:
                self.cartao_label.setText("Nenhum cartão cadastrado.")
                self.pagar_btn.setEnabled(False)

    def abrir_pix_window(self):
        pix_window = PixWindow(self.total, self)
        if pix_window.exec() == QDialog.Accepted:
            self.pix_confirmado = True
            self.pagar_btn.setEnabled(True)  # Habilitar o botão "Pagar" após gerar o PIX
            QMessageBox.information(self, "PIX Gerado", "QR Code gerado com sucesso. Clique em 'Pagar' para confirmar o pagamento.")
        else:
            self.pagar_btn.setEnabled(False)  # Desabilitar se o usuário cancelar

    def abrir_boleto_window(self):
        boleto_window = BoletoWindow(self.total, self)
        if boleto_window.exec() == QDialog.Accepted:
            self.boleto_confirmado = True
            self.pagar_btn.setEnabled(True)  # Habilitar o botão "Pagar" após gerar o boleto
            QMessageBox.information(self, "Boleto Gerado", "Boleto gerado com sucesso. Clique em 'Pagar' para confirmar o pagamento.")
        else:
            self.pagar_btn.setEnabled(False)  # Desabilitar se o usuário cancelar

    def confirmar_pagamento(self):
        forma_pagamento = self.pagamento_combo.currentText()
        print(f"Forma de pagamento selecionada: {forma_pagamento}")

        if forma_pagamento == "Cartão de Crédito/Débito":
            if not self.cartao_info:
                QMessageBox.warning(self, "Erro", "Nenhum cartão cadastrado. Por favor, adicione um cartão antes de prosseguir.")
                return
        elif forma_pagamento == "PIX":
            if not self.pix_confirmado:
                QMessageBox.warning(self, "Erro", "Por favor, gere o PIX e confirme o pagamento antes de prosseguir.")
                return
        elif forma_pagamento == "Boleto":
            if not self.boleto_confirmado:
                QMessageBox.warning(self, "Erro", "Por favor, gere o boleto e confirme o pagamento antes de prosseguir.")
                return

        print("Reservando assentos...")
        sucesso, mensagem = self.backend.reservar_assentos(self.usuario_id, self.sessao_id, self.assentos, forma_pagamento)
        print(f"Reserva retornou: sucesso={sucesso}, mensagem={mensagem}")

        if sucesso:
            QMessageBox.information(self, "Sucesso", mensagem)
            if not self.voltar_btn:
                self.voltar_btn = QPushButton("Voltar para a Home")
                self.voltar_btn.setStyleSheet("background-color: #e50914; color: #ffffff; border-radius: 8px; padding: 8px;")
                self.voltar_btn.clicked.connect(self.voltar_home)
                self.layout.addWidget(self.voltar_btn)
        else:
            QMessageBox.critical(self, "Erro", mensagem)

    def voltar_home(self):
        print("Fechando CompraWindow")
        self.close()

        # Fechar todas as janelas intermediárias (como SessaoWindow)
        parent = self.parent()
        while parent and isinstance(parent, QDialog):
            print(f"Fechando janela pai: {type(parent).__name__}")
            parent.close()
            parent = parent.parentWidget()

        # Validar se app_parent é válido
        if not self.app_parent:
            print("Erro: app_parent não está definido!")
            return

        # Garantir que a janela principal (CinemaApp) seja restaurada e exibida
        print("Restaurando janela principal")
        self.app_parent.show()  # Exibir a janela principal
        self.app_parent.showNormal()  # Restaura a janela principal se estiver minimizada
        self.app_parent.activateWindow()  # Traz a janela para o foco
        self.app_parent.raise_()  # Garante que a janela esteja na frente

        # Exibir a tela Home
        print("Exibindo Home")
        if hasattr(self.app_parent, 'clear_content') and hasattr(self.app_parent, 'show_home'):
            self.app_parent.clear_content()
            self.app_parent.show_home()
        else:
            print("Erro: app_parent não possui os métodos clear_content ou show_home!")

class CartaoWindow(QDialog):
    def __init__(self, backend, usuario_id, parent=None):
        super().__init__(parent)
        self.backend = backend
        self.usuario_id = usuario_id
        self.setWindowTitle("Dados do Cartão")
        self.setGeometry(300, 300, 300, 300)
        self.setStyleSheet("background-color: #1a1a1a;")
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Título
        title = QLabel("Adicionar/Alterar Cartão")
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: #ffffff;")
        layout.addWidget(title)

        # Campo Nome no Cartão
        self.nome_cartao = QLineEdit()
        self.nome_cartao.setPlaceholderText("Nome no Cartão")
        self.nome_cartao.setStyleSheet("background-color: #333333; color: #ffffff; padding: 5px;")
        layout.addWidget(self.nome_cartao)

        # Campo Número do Cartão
        self.numero_cartao = QLineEdit()
        self.numero_cartao.setPlaceholderText("Número do Cartão (16 dígitos)")
        self.numero_cartao.setStyleSheet("background-color: #333333; color: #ffffff; padding: 5px;")
        layout.addWidget(self.numero_cartao)

        # Campo Data de Expiração
        self.data_expiracao = QLineEdit()
        self.data_expiracao.setPlaceholderText("Data de Expiração (MM/AA)")
        self.data_expiracao.setStyleSheet("background-color: #333333; color: #ffffff; padding: 5px;")
        layout.addWidget(self.data_expiracao)

        # Campo CVV
        self.cvv = QLineEdit()
        self.cvv.setPlaceholderText("CVV (3 dígitos)")
        self.cvv.setStyleSheet("background-color: #333333; color: #ffffff; padding: 5px;")
        layout.addWidget(self.cvv)

        # Botão Salvar
        salvar_btn = QPushButton("Salvar Cartão")
        salvar_btn.setStyleSheet("background-color: #e50914; color: #ffffff; padding: 10px; border-radius: 8px;")
        salvar_btn.clicked.connect(self.salvar_cartao)
        layout.addWidget(salvar_btn)

        # Botão Cancelar
        cancelar_btn = QPushButton("Cancelar")
        cancelar_btn.setStyleSheet("background-color: #555555; color: #ffffff; padding: 10px; border-radius: 8px;")
        cancelar_btn.clicked.connect(self.close)
        layout.addWidget(cancelar_btn)

        self.setLayout(layout)

        # Preencher os campos se já houver um cartão cadastrado
        cartao_info = self.backend.get_cartao_info(self.usuario_id)
        if cartao_info:
            self.nome_cartao.setText(cartao_info[0])
            self.numero_cartao.setText(cartao_info[1])
            self.data_expiracao.setText(cartao_info[2])
            self.cvv.setText(cartao_info[3])

    def salvar_cartao(self):
        nome_cartao = self.nome_cartao.text().strip()
        numero_cartao = self.numero_cartao.text().strip()
        data_expiracao = self.data_expiracao.text().strip()
        cvv = self.cvv.text().strip()

        # Validação dos campos
        if not nome_cartao:
            QMessageBox.warning(self, "Erro", "Por favor, preencha o nome no cartão.")
            return
        if not numero_cartao or len(numero_cartao) != 16 or not numero_cartao.isdigit():
            QMessageBox.warning(self, "Erro", "O número do cartão deve conter exatamente 16 dígitos numéricos.")
            return
        if not data_expiracao or len(data_expiracao) != 5 or data_expiracao[2] != '/' or not all(c.isdigit() for c in data_expiracao.replace('/', '')):
            QMessageBox.warning(self, "Erro", "A data de expiração deve estar no formato MM/AA (ex.: 12/25).")
            return
        if not cvv or len(cvv) != 3 or not cvv.isdigit():
            QMessageBox.warning(self, "Erro", "O CVV deve conter exatamente 3 dígitos numéricos.")
            return

        # Salvar o cartão no backend
        try:
            self.backend.salvar_cartao(self.usuario_id, nome_cartao, numero_cartao, data_expiracao, cvv)
            QMessageBox.information(self, "Sucesso", "Cartão salvo com sucesso!")
            self.accept()  # Fecha o diálogo com sucesso
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao salvar o cartão: {str(e)}")

class PixWindow(QDialog):
    def __init__(self, total, parent=None):
        super().__init__(parent)
        self.total = total
        self.setWindowTitle("Pagamento via PIX")
        self.setGeometry(300, 300, 400, 300)
        self.setStyleSheet("background-color: #1a1a1a;")
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Título
        title = QLabel("Pague com PIX")
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: #ffffff;")
        layout.addWidget(title)

        # Valor Total
        layout.addWidget(QLabel(f"Valor Total: R${self.total:.2f}"))
        
        # Instruções
        instrucoes = QLabel("1. Abra o app do seu banco.\n2. Escaneie o QR Code abaixo.\n3. Confirme o pagamento.")
        instrucoes.setStyleSheet("color: #ffffff; font-size: 14px;")
        layout.addWidget(instrucoes)

        # QR Code Fictício (apenas um placeholder)
        qr_code = QLabel("QR Code Fictício\n[Imagine um QR Code aqui]")
        qr_code.setStyleSheet("background-color: #ffffff; color: #000000; padding: 10px; border-radius: 8px; qproperty-alignment: AlignCenter;")
        layout.addWidget(qr_code)

        # Botão Confirmar Pagamento
        confirmar_btn = QPushButton("Confirmar Pagamento")
        confirmar_btn.setStyleSheet("background-color: #e50914; color: #ffffff; padding: 10px; border-radius: 8px;")
        confirmar_btn.clicked.connect(self.accept)
        layout.addWidget(confirmar_btn)

        # Botão Cancelar
        cancelar_btn = QPushButton("Cancelar")
        cancelar_btn.setStyleSheet("background-color: #555555; color: #ffffff; padding: 10px; border-radius: 8px;")
        cancelar_btn.clicked.connect(self.reject)
        layout.addWidget(cancelar_btn)

        self.setLayout(layout)

class BoletoWindow(QDialog):
    def __init__(self, total, parent=None):
        super().__init__(parent)
        self.total = total
        self.setWindowTitle("Pagamento via Boleto")
        self.setGeometry(300, 300, 400, 300)
        self.setStyleSheet("background-color: #1a1a1a;")
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Título
        title = QLabel("Pague com Boleto")
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: #ffffff;")
        layout.addWidget(title)

        # Valor Total
        layout.addWidget(QLabel(f"Valor Total: R${self.total:.2f}"))

        # Instruções
        instrucoes = QLabel("1. Copie o código de barras abaixo.\n2. Pague no app do seu banco ou em uma lotérica.\n3. O pagamento pode levar até 3 dias úteis para ser compensado.")
        instrucoes.setStyleSheet("color: #ffffff; font-size: 14px;")
        layout.addWidget(instrucoes)

        # Código de Barras Fictício
        codigo_barras = QLabel("12345.67890 12345.678901 12345.678901 1 23456789012345")
        codigo_barras.setStyleSheet("background-color: #ffffff; color: #000000; padding: 10px; border-radius: 8px; qproperty-alignment: AlignCenter; font-family: monospace;")
        layout.addWidget(codigo_barras)

        # Botão Confirmar Pagamento
        confirmar_btn = QPushButton("Confirmar Pagamento")
        confirmar_btn.setStyleSheet("background-color: #e50914; color: #ffffff; padding: 10px; border-radius: 8px;")
        confirmar_btn.clicked.connect(self.accept)
        layout.addWidget(confirmar_btn)

        # Botão Cancelar
        cancelar_btn = QPushButton("Cancelar")
        cancelar_btn.setStyleSheet("background-color: #555555; color: #ffffff; padding: 10px; border-radius: 8px;")
        cancelar_btn.clicked.connect(self.reject)
        layout.addWidget(cancelar_btn)

        self.setLayout(layout)

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

    def closeEvent(self, event):
        print("Fechando a conexão com o banco de dados...")
        try:
            # Consumir quaisquer resultados pendentes
            while self.backend.cursor.nextset():
                pass
            self.backend.fechar_conexao()
        except Exception as e:
            print(f"Erro ao fechar a conexão: {e}")
        event.accept()

    def show_main_window(self, usuario_id, usuario_nome):
        self.main_layout.removeWidget(self.login_screen)
        self.login_screen.deleteLater()

        self.usuario_id = usuario_id
        self.usuario_nome = usuario_nome

        self.nav_bar = QHBoxLayout()
        self.nav_buttons = []  # Inicializar a lista de botões
        self.nav_bar.addWidget(self.create_nav_icon("🏠 Home", self.show_home))
        self.nav_bar.addWidget(self.create_nav_icon("⭐ Favoritos", self.show_favoritos))
        self.nav_bar.addWidget(self.create_nav_icon("🎟️ Compras", self.show_compras))
        self.nav_bar.addWidget(self.create_nav_icon("👤 Perfil", self.show_perfil))
        self.nav_bar.addWidget(self.create_nav_icon("🚪 Sair", self.logout))
        self.main_layout.addLayout(self.nav_bar)

        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.main_layout.addWidget(self.content_widget)

        self.show_home()

    def logout(self):
        print("Solicitando confirmação de logout...")
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Confirmação de Logout")
        msg_box.setText("Tem certeza que deseja sair da sua conta?")
        msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        msg_box.setDefaultButton(QMessageBox.StandardButton.No)
        
        msg_box.setStyleSheet("""
            QMessageBox {
                background-color: #ffffff;
                color: #000000;
            }
            QMessageBox QLabel {
                color: #000000;
            }
            QMessageBox QPushButton {
                background-color: #4CAF50;
                color: #ffffff;
                padding: 10px;
                border-radius: 3px;
            }
            QMessageBox QPushButton:hover {
                background-color: #45a049;
            }
        """)

        reply = msg_box.exec()

        if reply == QMessageBox.StandardButton.Yes:
            print("Usuário confirmou o logout.")
            self.clear_content()
            for i in reversed(range(self.main_layout.count())):
                widget = self.main_layout.itemAt(i).widget()
                if widget:
                    widget.deleteLater()
            
            for i in reversed(range(self.nav_bar.count())):
                widget = self.nav_bar.itemAt(i).widget()
                if widget:
                    widget.deleteLater()
            
            self.nav_buttons = []  # Limpar a lista de botões
            self.usuario_id = None
            self.usuario_nome = None
            
            self.login_screen = LoginWindow(self)
            self.main_layout.addWidget(self.login_screen)
            print("Logout concluído. Tela de login exibida.")
        else:
            print("Logout cancelado pelo usuário.")

    def create_nav_icon(self, icon, callback):
        btn = QPushButton(icon)
        btn.setStyleSheet("background-color: #2a2a2a; color: #ffffff; padding: 10px; border-radius: 8px;")
        btn.clicked.connect(lambda: self.handle_navigation(callback))
        if not hasattr(self, 'nav_buttons'):
            self.nav_buttons = []
        self.nav_buttons.append(btn)
        return btn

    def handle_navigation(self, callback):
        # Desabilitar todos os botões de navegação
        for btn in self.nav_buttons:
            btn.setEnabled(False)
        
        try:
            # Chamar a função de navegação (show_home, show_favoritos, etc.)
            callback()
        finally:
            # Reabilitar os botões após o carregamento
            for btn in self.nav_buttons:
                btn.setEnabled(True)

    def clear_content(self):
        print("Limpando conteúdo atual")
        for i in reversed(range(self.content_layout.count())):
            widget = self.content_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

    def show_home(self):
        print("Chamando show_home")
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
        print("Tela Home exibida com sucesso")

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
            compra_label = QLabel(f"{compra[1]} - {compra[2]} - {compra[3]} - Assento: {compra[4]}")
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

class PosterWidget(QWidget):
    def __init__(self, backend, usuario_id, filme_id, filme_nome, parent=None):
        super().__init__(parent)
        self.filme_id = filme_id
        self.filme_nome = filme_nome
        self.backend = backend
        self.usuario_id = usuario_id  # Adicionar usuario_id para uso em SessaoWindow
        self.parent = parent  # Garantir que o parent seja armazenado corretamente
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        # Obter informações do filme, incluindo o caminho do pôster
        filme_info = self.backend.get_filme_info(self.filme_id)
        poster_url = filme_info[9] if filme_info and len(filme_info) > 9 else None  # Índice 9 é o poster_path (agora uma URL)

        self.poster_label = QLabel()
        self.poster_label.setAlignment(Qt.AlignCenter)
        self.poster_label.setStyleSheet("background-color: #333; border-radius: 8px; padding: 10px; min-height: 150px;")

        print(f"Filme: {self.filme_nome}, Poster URL: {poster_url}")
        if poster_url:
            try:
                # Baixar a imagem da URL
                response = requests.get(poster_url, timeout=5)
                response.raise_for_status()  # Levanta uma exceção se a requisição falhar
                image_data = response.content

                # Carregar a imagem no QPixmap
                pixmap = QPixmap()
                pixmap.loadFromData(QByteArray(image_data))
                if not pixmap.isNull():
                    pixmap = pixmap.scaled(150, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                    self.poster_label.setPixmap(pixmap)
                else:
                    print(f"Erro: Não foi possível carregar a imagem da URL {poster_url}")
                    self.load_default_poster()
            except Exception as e:
                print(f"Erro ao baixar a imagem da URL {poster_url}: {str(e)}")
                self.load_default_poster()
        else:
            print(f"Erro: URL do pôster não definida para {self.filme_nome}")
            self.load_default_poster()

        self.poster_label.mousePressEvent = self.abrir_info_filme  # Conectar o clique à função abrir_info_filme
        layout.addWidget(self.poster_label)

        # Botão "Comprar Ingresso"
        comprar_btn = QPushButton("Comprar Ingresso")
        comprar_btn.clicked.connect(self.abrir_info_filme)  # Conectar o botão à função abrir_info_filme
        layout.addWidget(comprar_btn)

    def load_default_poster(self):
        """Carrega uma imagem padrão se a URL falhar."""
        default_image_url = "https://br.web.img3.acsta.net/pictures/14/02/18/17/30/589706.jpg"  # Imagem de Shrek como fallback
        try:
            response = requests.get(default_image_url, timeout=5)
            response.raise_for_status()
            image_data = response.content
            pixmap = QPixmap()
            pixmap.loadFromData(QByteArray(image_data))
            if not pixmap.isNull():
                pixmap = pixmap.scaled(150, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.poster_label.setPixmap(pixmap)
            else:
                self.poster_label.setText(f"Pôster não encontrado\n{self.filme_nome}")
        except Exception as e:
            print(f"Erro ao carregar a imagem padrão: {str(e)}")
            self.poster_label.setText(f"Pôster não encontrado\n{self.filme_nome}")

    def abrir_info_filme(self, event=None):
        """Abre a janela de informações do filme ao clicar no pôster ou no botão."""
        # Criar e exibir a janela de informações do filme
        self.filme_info_window = FilmeInfoWindow(self.filme_id, self.filme_nome, self.backend, self.parent)
        self.filme_info_window.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CinemaApp()
    window.show()
    sys.exit(app.exec())