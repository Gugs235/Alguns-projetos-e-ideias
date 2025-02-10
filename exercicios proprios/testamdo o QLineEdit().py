from PySide6.QtWidgets import QApplication, QLineEdit, QWidget, QVBoxLayout
import sys

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.input_text = QLineEdit(self)
        self.input_text.setPlaceholderText("Digite algo aqui...")
        self.input_text.setMaxLength(20)  # Limite de caracteres
        self.input_text.setStyleSheet("font-size: 18px; padding: 5px;")  # Estilização
        self.input_text.setMinimumSize(150, 30)  # Tamanho mínimo permitido
        self.input_text.setMaximumSize(400, 50)  # Tamanho máximo permitido

        self.input_text.setEchoMode(QLineEdit.Password)  # Esconde a entrada (como senha)

        layout = QVBoxLayout()
        layout.addWidget(self.input_text)
        self.setLayout(layout)

app = QApplication(sys.argv)
window = MyWindow()
window.show()
sys.exit(app.exec())


#.....................#


import sys
from PySide6.QtWidgets import QApplication, QLabel, QLineEdit, QVBoxLayout, QWidget, QPushButton, QMessageBox
from PySide6.QtCore import Qt


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Login")
        self.resize(400, 300)  # Tamanho inicial da janela

        self.label_username = QLabel("Usuário:")
        self.label_username.setAlignment(Qt.AlignCenter)
        self.label_username.setStyleSheet("font-size: 24px; font-weight: bold;")
        self.input_username = QLineEdit()
        self.input_username.setStyleSheet("font-size: 18px; padding: 5px;")  
        self.input_username.setMinimumSize(150, 30)
        self.input_username.setMaximumSize(400, 50)

        self.label_password = QLabel("Senha:")
        self.label_password.setAlignment(Qt.AlignCenter)
        self.label_password.setStyleSheet("font-size: 24px; font-weight: bold;")
        self.input_password = QLineEdit()
        self.input_password.setEchoMode(QLineEdit.Password)
        self.input_password.setStyleSheet("font-size: 18px; padding: 5px;")  
        self.input_password.setMinimumSize(150, 30)
        self.input_password.setMaximumSize(400, 50)

        self.button_login = QPushButton("Entrar")
        self.button_login.setStyleSheet("font-size: 24px; font-weight: bold;")
        self.button_login.clicked.connect(self.check_login)

        layout = QVBoxLayout()
        layout.addWidget(self.label_username)
        layout.addWidget(self.input_username)
        layout.addWidget(self.label_password)
        layout.addWidget(self.input_password)
        layout.addWidget(self.button_login)
        layout.setAlignment(Qt.AlignCenter)  # 🔹 Centraliza o layout na janela

        self.setLayout(layout)
        self.centralizar_janela()  # 🔹 Centraliza ao abrir

    def centralizar_janela(self):
        """Função para centralizar a janela na tela"""
        screen_geometry = QApplication.primaryScreen().geometry()
        window_geometry = self.frameGeometry()
        center_x = (screen_geometry.width() - window_geometry.width()) // 2
        center_y = (screen_geometry.height() - window_geometry.height()) // 2
        self.move(center_x, center_y)

    def resizeEvent(self, event):
        """Redimensiona e mantém os elementos centralizados quando a janela for maximizada."""
        self.centralizar_janela()  # 🔹 Mantém a centralização
        super().resizeEvent(event)  # 🔹 Continua o comportamento padrão de redimensionamento

    def check_login(self):
        correct_username = "Jss"
        correct_password = "jss235"

        username = self.input_username.text()
        password = self.input_password.text()

        if username == correct_username and password == correct_password:
            QMessageBox.information(self, "Login feito com sucesso", "Bem-vindo, " + username + "!")
            QApplication.quit()
        else:    
            QMessageBox.warning(self, "Erro no Login", "Usuário ou senha incorretos.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec())
