# main.py
import sys
from frontend import CinemaApp
from PySide6.QtWidgets import QApplication

def main():
    print("Abrindo o sistema de check-in de cinema...")
    app = QApplication(sys.argv)
    window = CinemaApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()