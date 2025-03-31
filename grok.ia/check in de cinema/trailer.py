import sys
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                               QLabel, QComboBox, QPushButton, QSizePolicy)
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import Qt

class FilmeDetalhes(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Stitch: Live Action - Compra de Ingressos")
        self.setGeometry(100, 100, 800, 600)
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignCenter)
        main_layout.setSpacing(15)

        # Trailer do YouTube centralizado
        video_container = QWidget()
        video_layout = QHBoxLayout(video_container)
        video_layout.setAlignment(Qt.AlignCenter)

        self.web_view = QWebEngineView()
        self.web_view.setFixedSize(640, 360)  # Tamanho padrão 16:9
        video_id = "oLnS1Ij9-Kk"  # ID do trailer do Stitch
        html = f"""
        <iframe width="640" height="360"
                src="https://www.youtube.com/embed/{video_id}"
                frameborder="0"
                allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture"
                allowfullscreen>
        </iframe>
        """
        self.web_view.setHtml(html)
        video_layout.addWidget(self.web_view)
        main_layout.addWidget(video_container)

        # Sinopse do filme Stitch Live Action
        sinopse_text = ("Sinopse: Em 'Stitch: Live Action', o adorável experimento alienígena 626 "
                        "chega ao Havaí em uma aventura emocionante. Lilo, agora crescida, enfrenta "
                        "novos desafios enquanto Stitch tenta se adaptar à vida terrestre, "
                        "enfrentando ameaças intergalácticas e fortalecendo os laços de ohana.")
        sinopse_label = QLabel(sinopse_text)
        sinopse_label.setWordWrap(True)
        sinopse_label.setAlignment(Qt.AlignCenter)
        sinopse_label.setStyleSheet("font-size: 14px; padding: 10px;")
        main_layout.addWidget(sinopse_label)

        # Seleção de assentos e horários
        options_layout = QHBoxLayout()
        options_layout.setSpacing(20)

        # Horários
        horarios_widget = QWidget()
        horarios_layout = QVBoxLayout(horarios_widget)
        horarios_label = QLabel("Escolha o Horário:")
        horarios_label.setStyleSheet("font-weight: bold;")
        self.horarios_combo = QComboBox()
        self.horarios_combo.addItems(["15:00", "18:00", "21:00"])
        self.horarios_combo.setFixedWidth(100)
        horarios_layout.addWidget(horarios_label)
        horarios_layout.addWidget(self.horarios_combo)
        options_layout.addWidget(horarios_widget)

        # Assentos
        assentos_widget = QWidget()
        assentos_layout = QVBoxLayout(assentos_widget)
        assentos_label = QLabel("Escolha o Assento:")
        assentos_label.setStyleSheet("font-weight: bold;")
        self.assentos_combo = QComboBox()
        assentos_disponiveis = ["A2", "A3", "B5", "B6", "C1", "C2"]
        self.assentos_combo.addItems(assentos_disponiveis)
        self.assentos_combo.setFixedWidth(100)
        assentos_layout.addWidget(assentos_label)
        assentos_layout.addWidget(self.assentos_combo)
        options_layout.addWidget(assentos_widget)

        main_layout.addLayout(options_layout)

        # Botão Comprar Ingresso (vermelho)
        self.comprar_button = QPushButton("Comprar Ingresso")
        self.comprar_button.setStyleSheet("""
            QPushButton {
                background-color: #ff0000;
                color: white;
                padding: 10px;
                font-size: 16px;
                font-weight: bold;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #cc0000;
            }
        """)
        self.comprar_button.setFixedWidth(200)
        self.comprar_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        main_layout.addWidget(self.comprar_button, alignment=Qt.AlignCenter)

        # Conectar o botão
        self.comprar_button.clicked.connect(self.comprar_ingresso)

        # Espaçador no final
        main_layout.addStretch()

    def comprar_ingresso(self):
        horario = self.horarios_combo.currentText()
        assento = self.assentos_combo.currentText()
        mensagem = f"Ingresso comprado!\nHorário: {horario}\nAssento: {assento}"
        print(mensagem)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FilmeDetalhes()
    window.show()
    sys.exit(app.exec())
