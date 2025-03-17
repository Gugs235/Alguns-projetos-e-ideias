# frontend.py
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QMessageBox, QScrollArea, QGridLayout, QDialog, QComboBox, QListWidget, QTextEdit
from PySide6.QtCore import Qt, QSize, QUrl
from backend import CinemaBackend
import sys
import os
from PySide6.QtMultimedia import QMediaPlayer
from PySide6.QtMultimediaWidgets import QVideoWidget
import yt_dlp

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
    def __init__(self, backend, usuario_id, filme_id, app_parent, parent=None):
        super().__init__(parent)
        self.backend = backend
        self.usuario_id = usuario_id
        self.filme_id = filme_id
        self.app_parent = app_parent  # Referência ao CinemaApp
        self.setWindowTitle("Informações do Filme")
        self.init_ui()

    def favoritar_filme(self):
        sucesso, mensagem = self.backend.adicionar_favorito(self.usuario_id, self.filme_id)
        if sucesso:
            QMessageBox.information(self, "Sucesso", mensagem)
        else:
            QMessageBox.critical(self, "Erro", mensagem)

    def abrir_selecao_sessao(self):
        self.sessao_window = SessaoWindow(self.backend, self.usuario_id, self.filme_id, self.app_parent, self)
        self.sessao_window.exec()

    def get_youtube_video_url(self, youtube_url):
        try:
            ydl_opts = {
                'format': 'bestvideo[height<=480]+bestaudio/best[height<=480]',  # Limita a 480p para compatibilidade
                'quiet': True,
                'no_warnings': True,
                'merge_output_format': 'mp4',  # Força formato MP4
                'outtmpl': '-',  # Não baixa, apenas retorna a URL
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(youtube_url, download=False)
                if 'url' in info.get('formats', [{}])[0]:
                    return info.get('formats', [{}])[0]['url']
                else:
                    print(f"Erro: 'url' não encontrado na resposta do yt-dlp para {youtube_url}")
                    return None
        except Exception as e:
            print(f"Erro ao extrair URL do YouTube: {str(e)}")
            return None

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(10, 10, 10, 10)

        filme_info = self.backend.get_filme_info(self.filme_id)
        title_label = QLabel(filme_info[1])
        title_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #ffffff; padding: 5px;")
        layout.addWidget(title_label)

        trailer_label = QLabel("Trailer:")
        trailer_label.setStyleSheet("color: #ffffff; font-size: 16px; font-weight: bold;")
        layout.addWidget(trailer_label)
        self.video_widget = QVideoWidget()
        self.video_widget.setFixedSize(400, 200)
        layout.addWidget(self.video_widget)
        self.media_player = QMediaPlayer(self)
        self.media_player.setVideoOutput(self.video_widget)

        youtube_url = filme_info[8]  # URL do trailer do filme
        video_url = self.get_youtube_video_url(youtube_url)
        if video_url:
            trailer_url = QUrl(video_url)
            self.media_player.setSource(trailer_url)
            self.media_player.play()
            self.media_player.error.connect(lambda: print(f"Erro ao reproduzir o vídeo: {self.media_player.errorString()}"))
        else:
            error_label = QLabel(f"Não foi possível carregar o trailer para {filme_info[1]}. Verifique a URL ou a conexão.")
            error_label.setStyleSheet("color: #ff5555; font-size: 14px;")
            layout.addWidget(error_label)

        # Restante do código (informações adicionais, botões, etc.)
        info_layout = QVBoxLayout()
        info_layout.addWidget(QLabel(f"Duração: {filme_info[3]}"))
        info_layout.addWidget(QLabel(f"Data de Lançamento: {filme_info[4]}"))
        info_layout.addWidget(QLabel(f"Gênero: {filme_info[5]}"))
        info_layout.addWidget(QLabel(f"Classificação: {filme_info[6]}"))

        sinopse_widget = QWidget()
        sinopse_layout = QVBoxLayout(sinopse_widget)
        sinopse_label = QLabel("Sinopse:")
        sinopse_label.setStyleSheet("color: #ffffff; font-size: 16px; font-weight: bold;")
        sinopse_text = QTextEdit(filme_info[7])
        sinopse_text.setReadOnly(True)
        sinopse_text.setFixedHeight(100)
        sinopse_text.setStyleSheet("background-color: #2a2a2a; color: #ffffff; border: 1px solid #444; border-radius: 5px; padding: 5px;")
        sinopse_layout.addWidget(sinopse_label)
        sinopse_layout.addWidget(sinopse_text)
        info_layout.addWidget(sinopse_widget)

        layout.addLayout(info_layout)

        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
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
        self.setMinimumSize(400, 600)
        self.adjustSize()

class SessaoWindow(QDialog):
    def __init__(self, backend, usuario_id, filme_id, app_parent, parent=None):
        super().__init__(parent)
        self.backend = backend
        self.usuario_id = usuario_id
        self.filme_id = filme_id
        self.app_parent = app_parent
        self.selected_assentos = []  # Inicializa a lista de assentos selecionados
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

    def abrir_compra(self):
        if not hasattr(self, 'selected_assentos') or not self.selected_assentos:
            QMessageBox.warning(self, "Erro", "Selecione pelo menos um assento!")
            return
        self.compra_window = CompraWindow(self.backend, self.usuario_id, self.filme_id, self.selected_sessao_id, self.selected_assentos, self.app_parent, self)
        self.compra_window.exec()

    def atualizar_assentos(self):
        for i in range(self.assentos_grid.count()):
            self.assentos_grid.itemAt(i).widget().deleteLater()
        self.assentos.clear()

        assentos_disponiveis = self.backend.get_assentos_disponiveis(self.selected_sessao_id)
        _, maxima = self.backend.get_lotacao_atual(self.selected_sessao_id)
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
            # Verifica se o assento já está selecionado antes de adicionar
            if assento not in self.selected_assentos and len(self.selected_assentos) < 10:  # Limite de 10 assentos por compra
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
        self.voltar_btn = None  # Inicializa como None
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
        print(f"Forma de pagamento selecionada: {forma_pagamento}")  # Depuração
        if forma_pagamento == "Cartão de Crédito/Débito":
            nome_cartao = self.nome_cartao.text().strip()
            numero_cartao = self.numero_cartao.text().strip()
            data_expiracao = self.data_expiracao.text().strip()
            cvv = self.cvv.text().strip()

            print(f"Campos: Nome={nome_cartao}, Número={numero_cartao}, Data={data_expiracao}, CVV={cvv}")  # Depuração
            if not all([nome_cartao, numero_cartao, data_expiracao, cvv]):
                QMessageBox.warning(self, "Erro", "Preencha todos os campos do cartão!")
                return
            if len(numero_cartao) != 16 or not numero_cartao.isdigit():
                QMessageBox.warning(self, "Erro", "O número do cartão deve ter exatamente 16 dígitos numéricos!")
                return
            if len(data_expiracao) != 5 or data_expiracao[2] != '/' or not all(c.isdigit() for c in data_expiracao.replace('/', '')):
                QMessageBox.warning(self, "Erro", "A data de expiração deve estar no formato MM/AA!")
                return
            if len(cvv) != 3 or not cvv.isdigit():
                QMessageBox.warning(self, "Erro", "O CVV deve ter exatamente 3 dígitos numéricos!")
                return

            print("Salvando cartão no backend...")  # Depuração
            self.backend.salvar_cartao(self.usuario_id, nome_cartao, numero_cartao, data_expiracao, cvv)

        print("Reservando assentos...")  # Depuração
        sucesso, mensagem = self.backend.reservar_assentos(self.usuario_id, self.sessao_id, self.assentos, forma_pagamento)
        print(f"Reserva retornou: sucesso={sucesso}, mensagem={mensagem}")  # Depuração

        if sucesso:
            QMessageBox.information(self, "Sucesso", mensagem)
            if not self.voltar_btn:  # Adiciona o botão apenas se não existir
                self.voltar_btn = QPushButton("Voltar para a Home")
                self.voltar_btn.clicked.connect(self.voltar_home)
                self.layout().addWidget(self.voltar_btn)
        else:
            QMessageBox.critical(self, "Erro", mensagem)

    def voltar_home(self):
        self.app_parent.show_home()  # Usa a referência direta
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
        self.nav_bar.addWidget(self.create_nav_icon("🏠 Home", self.show_home))
        self.nav_bar.addWidget(self.create_nav_icon("⭐ Favoritos", self.show_favoritos))
        self.nav_bar.addWidget(self.create_nav_icon("🎟️ Compras", self.show_compras))
        self.nav_bar.addWidget(self.create_nav_icon("👤 Perfil", self.show_perfil))
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
        info_window = FilmeInfoWindow(self.backend, self.usuario_id, self.filme_id, self.parent(), self.parent())
        info_window.exec()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CinemaApp()
    window.show()
    sys.exit(app.exec())