# Check-in de Cinema 3.0

from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QComboBox, QMessageBox
import sys
import sqlite3

# Função para configurar o banco de dados inicial
def inicializar_banco():
    conexao = sqlite3.connect("cinema.db")
    cursor = conexao.cursor()
    
    # Criando tabelas para armazenar cinemas, filmes e assentos
    cursor.executescript('''
        CREATE TABLE IF NOT EXISTS cinemas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT
        );

        CREATE TABLE IF NOT EXISTS filmes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cinema_id INTEGER,
            nome TEXT,
            FOREIGN KEY (cinema_id) REFERENCES cinemas(id)
        );

        CREATE TABLE IF NOT EXISTS assentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filme_id INTEGER,
            assento TEXT,
            ocupado INTEGER DEFAULT 0,
            FOREIGN KEY (filme_id) REFERENCES filmes(id)
        );
    ''')
    
    # Inserindo alguns cinemas no banco caso ainda não existam
    cursor.execute("SELECT COUNT(*) FROM cinemas")
    if cursor.fetchone()[0] == 0:
        cursor.executemany("INSERT INTO cinemas (nome) VALUES (?)", [
            ("Cinépolis Campo Grande",),
            ("UCI Bosque dos Ipês",),
            ("Cinemark Norte Sul Plaza",)
        ])
    
    # Inserindo alguns filmes no banco caso ainda não existam
    cursor.execute("SELECT COUNT(*) FROM filmes")
    if cursor.fetchone()[0] == 0:
        cursor.executemany("INSERT INTO filmes (cinema_id, nome) VALUES (?, ?)", [
            (1, "Duna: Parte 2"),
            (1, "Homem-Aranha: Além do Aranhaverso"),
            (2, "Oppenheimer"),
            (2, "Barbie"),
            (3, "Velozes e Furiosos 10"),
            (3, "Avatar 2")
        ])

    conexao.commit()
    conexao.close()

# Tela principal do programa
class TelaPrincipal(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Check-in de Cinema")
        self.setGeometry(100, 100, 400, 300)
        self.layout = QVBoxLayout()
        
        self.label_cinema = QLabel("Escolha o Cinema:")
        self.combo_cinema = QComboBox()
        self.botao_continuar = QPushButton("Continuar")
        
        self.layout.addWidget(self.label_cinema)
        self.layout.addWidget(self.combo_cinema)
        self.layout.addWidget(self.botao_continuar)
        
        self.setLayout(self.layout)

        self.carregar_cinemas()
        self.botao_continuar.clicked.connect(self.ir_para_filmes)

    # Carrega os cinemas disponíveis no banco de dados
    def carregar_cinemas(self):
        conexao = sqlite3.connect("cinema.db")
        cursor = conexao.cursor()
        cursor.execute("SELECT id, nome FROM cinemas")
        self.cinemas = cursor.fetchall()
        conexao.close()
        
        for cinema in self.cinemas:
            self.combo_cinema.addItem(cinema[1], cinema[0])

    # Abre a tela de escolha de filmes
    def ir_para_filmes(self):
        cinema_id = self.combo_cinema.currentData()
        self.filme_tela = TelaFilme(cinema_id)
        self.filme_tela.show()
        self.close()

# Tela de seleção de filme
class TelaFilme(QWidget):
    def __init__(self, cinema_id):
        super().__init__()
        self.setWindowTitle("Escolha do Filme")
        self.setGeometry(100, 100, 400, 300)
        self.layout = QVBoxLayout()
        
        self.label_filme = QLabel("Escolha o Filme:")
        self.combo_filme = QComboBox()
        self.botao_continuar = QPushButton("Continuar")

        self.layout.addWidget(self.label_filme)
        self.layout.addWidget(self.combo_filme)
        self.layout.addWidget(self.botao_continuar)
        
        self.setLayout(self.layout)
        
        self.cinema_id = cinema_id
        self.carregar_filmes()
        self.botao_continuar.clicked.connect(self.ir_para_assentos)

    # Carrega os filmes disponíveis no cinema selecionado
    def carregar_filmes(self):
        conexao = sqlite3.connect("cinema.db")
        cursor = conexao.cursor()
        cursor.execute("SELECT id, nome FROM filmes WHERE cinema_id = ?", (self.cinema_id,))
        self.filmes = cursor.fetchall()
        conexao.close()

        for filme in self.filmes:
            self.combo_filme.addItem(filme[1], filme[0])

    # Abre a tela de seleção de assentos
    def ir_para_assentos(self):
        filme_id = self.combo_filme.currentData()
        self.assento_tela = TelaAssento(filme_id)
        self.assento_tela.show()
        self.close()

# Tela de seleção de assento
class TelaAssento(QWidget):
    def __init__(self, filme_id):
        super().__init__()
        self.setWindowTitle("Escolha seu Assento")
        self.setGeometry(100, 100, 400, 300)
        self.layout = QVBoxLayout()
        
        self.label_assento = QLabel("Escolha um Assento Disponível:")
        self.combo_assento = QComboBox()
        self.botao_continuar = QPushButton("Continuar")

        self.layout.addWidget(self.label_assento)
        self.layout.addWidget(self.combo_assento)
        self.layout.addWidget(self.botao_continuar)
        
        self.setLayout(self.layout)
        
        self.filme_id = filme_id
        self.carregar_assentos()
        self.botao_continuar.clicked.connect(self.ir_para_pagamento)

    # Carrega os assentos disponíveis para o filme selecionado
    def carregar_assentos(self):
        conexao = sqlite3.connect("cinema.db")
        cursor = conexao.cursor()
        
        # Criando assentos caso ainda não existam
        cursor.execute("SELECT COUNT(*) FROM assentos WHERE filme_id = ?", (self.filme_id,))
        if cursor.fetchone()[0] == 0:
            assentos = [(self.filme_id, f"A{i}") for i in range(1, 11)]
            cursor.executemany("INSERT INTO assentos (filme_id, assento) VALUES (?, ?)", assentos)
            conexao.commit()

        cursor.execute("SELECT id, assento FROM assentos WHERE filme_id = ? AND ocupado = 0", (self.filme_id,))
        self.assentos_disponiveis = cursor.fetchall()
        conexao.close()

        for assento in self.assentos_disponiveis:
            self.combo_assento.addItem(assento[1], assento[0])

    # Abre a tela de pagamento
    def ir_para_pagamento(self):
        assento_id = self.combo_assento.currentData()
        self.pagamento_tela = TelaPagamento(assento_id)
        self.pagamento_tela.show()
        self.close()

# Tela de pagamento
class TelaPagamento(QWidget):
    def __init__(self, assento_id):
        super().__init__()
        self.setWindowTitle("Pagamento")
        self.setGeometry(100, 100, 400, 300)
        self.layout = QVBoxLayout()
        
        self.label_pagamento = QLabel("Escolha a Forma de Pagamento:")
        self.combo_pagamento = QComboBox()
        self.combo_pagamento.addItems(["Cartão de Crédito", "Cartão de Débito", "Pix", "Boleto"])
        self.botao_finalizar = QPushButton("Finalizar Compra")

        self.layout.addWidget(self.label_pagamento)
        self.layout.addWidget(self.combo_pagamento)
        self.layout.addWidget(self.botao_finalizar)
        
        self.setLayout(self.layout)
        self.assento_id = assento_id
        self.botao_finalizar.clicked.connect(self.finalizar)

    # Finaliza a compra e marca o assento como ocupado
    def finalizar(self):
        conexao = sqlite3.connect("cinema.db")
        cursor = conexao.cursor()
        cursor.execute("UPDATE assentos SET ocupado = 1 WHERE id = ?", (self.assento_id,))
        conexao.commit()
        conexao.close()

        QMessageBox.information(self, "Sucesso", "Compra finalizada!")
        self.close()

# Iniciando o aplicativo
if __name__ == "__main__":
    inicializar_banco()
    app = QApplication(sys.argv)
    tela = TelaPrincipal()
    tela.show()
    sys.exit(app.exec())
