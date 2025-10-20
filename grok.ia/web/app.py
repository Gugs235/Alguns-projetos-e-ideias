from flask import Flask, render_template, request, redirect, url_for, session, flash, send_from_directory
import os
from database import CinemaDatabase
from backend import CinemaBackend
import requests

app = Flask(__name__)
app.secret_key = 'chave_secreta_para_sessao'
app.config['UPLOAD_FOLDER'] = 'static/posters'

# Inicializar backend
db = CinemaDatabase()
backend = CinemaBackend()

@app.route('/')
def index():
    if 'usuario_id' in session:
        return redirect(url_for('home'))
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        usuario = backend.login_usuario(email, senha)
        if usuario:
            session['usuario_id'] = usuario[0]
            session['usuario_nome'] = usuario[1]
            return redirect(url_for('home'))
        else:
            flash('Email ou senha incorretos!')
    return render_template('login.html')

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        sobrenome = request.form['sobrenome']
        email = request.form['email']
        senha = request.form['senha']
        sucesso, mensagem = backend.cadastrar_usuario(nome, sobrenome, email, senha)
        if sucesso:
            flash('Cadastro realizado com sucesso! Faça login.')
            return redirect(url_for('login'))
        else:
            flash(mensagem)
    return render_template('cadastro.html')

@app.route('/home')
def home():
    if 'usuario_id' not in session:
        return redirect(url_for('index'))
    filmes = backend.get_filmes_all()
    return render_template('home.html', filmes=filmes)

@app.route('/filme/<int:filme_id>')
def filme(filme_id):
    if 'usuario_id' not in session:
        return redirect(url_for('index'))
    filme_info = backend.get_filme_info(filme_id)
    if not filme_info:
        flash('Filme não encontrado!')
        return redirect(url_for('home'))
    return render_template('filme.html', filme=filme_info)

@app.route('/favoritar/<int:filme_id>', methods=['POST'])
def favoritar(filme_id):
    if 'usuario_id' not in session:
        return redirect(url_for('index'))
    usuario_id = session['usuario_id']
    if backend.is_favorito(usuario_id, filme_id):
        backend.remover_favorito(usuario_id, filme_id)
    else:
        backend.adicionar_favorito(usuario_id, filme_id)
    return redirect(request.referrer or url_for('home'))

@app.route('/sessoes/<int:filme_id>')
def sessoes(filme_id):
    if 'usuario_id' not in session:
        return redirect(url_for('index'))
    sessoes = backend.get_sessoes_info(filme_id)
    filme_info = backend.get_filme_info(filme_id)
    return render_template('sessoes.html', sessoes=sessoes, filme=filme_info)

@app.route('/assentos/<int:sessao_id>', methods=['GET', 'POST'])
def assentos(sessao_id):
    if 'usuario_id' not in session:
        return redirect(url_for('index'))
    usuario_id = session['usuario_id']
    assentos_disponiveis = backend.get_assentos_disponiveis(sessao_id)
    if request.method == 'POST':
        assentos_selecionados = request.form.getlist('assentos')
        if not assentos_selecionados:
            flash('Selecione pelo menos um assento!')
            return redirect(url_for('assentos', sessao_id=sessao_id))
        session['assentos_selecionados'] = assentos_selecionados
        session['sessao_id'] = sessao_id
        return redirect(url_for('compra'))
    return render_template('assentos.html', assentos_disponiveis=assentos_disponiveis, sessao_id=sessao_id)

@app.route('/compra', methods=['GET', 'POST'])
def compra():
    if 'usuario_id' not in session or 'assentos_selecionados' not in session:
        return redirect(url_for('index'))
    usuario_id = session['usuario_id']
    sessao_id = session['sessao_id']
    assentos = session['assentos_selecionados']
    tipos_ingresso = backend.get_tipos_ingresso()
    preco_base = backend.get_preco_sessao(sessao_id)
    if request.method == 'POST':
        forma_pagamento = request.form['forma_pagamento']
        assentos_tipos = []
        for assento in assentos:
            tipo_id = request.form.get(f'tipo_{assento}')
            # Simular reserva (sem implementar pagamento real)
            assentos_tipos.append((assento, tipo_id))
        sucesso, mensagem = backend.reservar_assentos(usuario_id, sessao_id, assentos_tipos, forma_pagamento)
        if sucesso:
            flash('Compra realizada com sucesso!')
            session.pop('assentos_selecionados', None)
            session.pop('sessao_id', None)
            return redirect(url_for('home'))
        else:
            flash(mensagem)
    return render_template('compra.html', assentos=assentos, tipos_ingresso=tipos_ingresso, preco_base=preco_base)

@app.route('/favoritos')
def favoritos():
    if 'usuario_id' not in session:
        return redirect(url_for('index'))
    usuario_id = session['usuario_id']
    filmes = backend.get_favoritos(usuario_id)
    return render_template('favoritos.html', filmes=filmes)

@app.route('/compras')
def compras():
    if 'usuario_id' not in session:
        return redirect(url_for('index'))
    usuario_id = session['usuario_id']
    compras = backend.get_compras(usuario_id)
    return render_template('compras.html', compras=compras)

@app.route('/perfil')
def perfil():
    if 'usuario_id' not in session:
        return redirect(url_for('index'))
    usuario_id = session['usuario_id']
    usuario_info = backend.get_usuario_info(usuario_id)
    cartao_info = backend.get_cartao_info(usuario_id)
    return render_template('perfil.html', usuario=usuario_info, cartao=cartao_info)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/admin')
def admin():
    if 'admin' not in session:
        return redirect(url_for('admin_login'))
    return render_template('admin.html')

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == 'admin123':
            session['admin'] = True
            return redirect(url_for('admin'))
        else:
            flash('Credenciais inválidas!')
    return render_template('admin_login.html')

@app.route('/admin/cinemas')
def admin_cinemas():
    if 'admin' not in session:
        return redirect(url_for('admin_login'))
    cinemas = backend.get_cinemas_all()
    return render_template('admin_cinemas.html', cinemas=cinemas)

@app.route('/admin/filmes')
def admin_filmes():
    if 'admin' not in session:
        return redirect(url_for('admin_login'))
    filmes = backend.get_filmes_all()
    return render_template('admin_filmes.html', filmes=filmes)

@app.route('/admin/sessoes')
def admin_sessoes():
    if 'admin' not in session:
        return redirect(url_for('admin_login'))
    sessoes = backend.get_sessoes_all()
    return render_template('admin_sessoes.html', sessoes=sessoes)

@app.route('/poster/<filename>')
def poster(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
