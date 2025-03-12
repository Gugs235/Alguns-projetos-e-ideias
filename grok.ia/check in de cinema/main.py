# main.py
import sys
from database import init_db
from frontend import CinemaApp
from PySide6.QtWidgets import QApplication

def main():
    print("Inicializando o banco de dados...")
    init_db()
    print("Abrindo o sistema de check-in de cinema...")
    app = QApplication(sys.argv)
    window = CinemaApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()

