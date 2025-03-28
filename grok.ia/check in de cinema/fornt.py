    # def init_ui(self):
    #     layout = QVBoxLayout(self)

    #     # Logo e Nome da Empresa
    #     logo = QLabel("🎬 PobreVision")
    #     logo.setStyleSheet("font-size: 40px; color: #e50914; font-weight: bold; padding: 20px;")
    #     logo.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Centralizar o logo
    #     layout.addWidget(logo)

    #     # Cards com Imagens de Filmes
    #     cards_layout = QHBoxLayout()
    #     for i in range(3):
    #         card = QLabel(f"Filme {i+1}")
    #         card.setStyleSheet("""
    #             background-color: #333;
    #             border-radius: 8px;
    #             padding: 10px;
    #             min-width: 150px;
    #             min-height: 200px;
    #             qproperty-alignment: AlignCenter;
    #         """)
    #         cards_layout.addWidget(card)
    #     cards_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Centralizar os cards
    #     layout.addLayout(cards_layout)

    #     # Texto de Boas-Vindas
    #     welcome_text = QLabel("Bem-vindo ao PobreVision! Faça login ou cadastre-se para comprar ingressos.")
    #     welcome_text.setStyleSheet("font-size: 16px; color: #ffffff; padding: 10px;")
    #     welcome_text.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Centralizar o texto
    #     layout.addWidget(welcome_text)

    #     # Espaçador superior para empurrar os botões para o centro verticalmente
    #     layout.addStretch(1)

    #     # Layout horizontal para os botões
    #     buttons_layout = QHBoxLayout()

    #     # Botão Login
    #     self.login_btn = QPushButton("Login")
    #     self.login_btn.setMinimumSize(QSize(100, 40))
    #     self.login_btn.setMaximumSize(QSize(100, 40))
    #     self.login_btn.clicked.connect(self.show_login_form)
    #     self.login_btn.setStyleSheet("background-color: #e50914; color: #ffffff; padding: 10px; border-radius: 8px;")
    #     buttons_layout.addWidget(self.login_btn)

    #     # Espaçador entre os botões
    #     buttons_layout.addSpacing(20)  # Adiciona um espaço de 20px entre os botões

    #     # Botão Cadastrar
    #     self.cadastro_btn = QPushButton("Cadastrar")
    #     self.cadastro_btn.setMinimumSize(QSize(100, 40))
    #     self.cadastro_btn.setMaximumSize(QSize(100, 40))
    #     self.cadastro_btn.clicked.connect(self.show_cadastro_form)
    #     self.cadastro_btn.setStyleSheet("background-color: #e50914; color: #ffffff; padding: 10px; border-radius: 8px;")
    #     buttons_layout.addWidget(self.cadastro_btn)

    #     # Centralizar o layout dos botões horizontalmente
    #     buttons_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

    #     # Adicionar o layout dos botões ao layout principal
    #     layout.addLayout(buttons_layout)

    #     # Espaçador inferior para equilibrar o centralização vertical
    #     layout.addStretch(1)

    #     self.setStyleSheet("background-color: #1a1a1a;")