from flask import render_template, request, redirect, session, flash, url_for, send_from_directory
from coletaon import app, db
from models import Agendamentos
from helpers import recupera_imagem, deleta_arquivo, FormularioAgendamento
import time


@app.route('/')
def index():
    lista = Agendamentos.query.order_by(Agendamentos.id)
    return render_template('lista.html', titulo="Cooperativa - Coleta ON - Lista de Agendamentos", agendamentos=lista)

@app.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('novo')))
    form = FormularioAgendamento()
    return render_template('novo.html', titulo='Novo Agendamento', form=form)

@app.route('/criar', methods=['POST',])
def criar():
    form= FormularioAgendamento(request.form)

    if not form.validate_on_submit():
        return redirect(url_for('novo'))

    nome = form.nome.data
    endereco = form.endereco.data
    data_dia = form.data_dia.data
    horario = form.horario.data

    agendamento = Agendamentos.query.filter_by(nome=nome).first()

    if agendamento:
        flash('Agendamento já existente!')
        return redirect(url_for('index'))

    novo_agendamento = Agendamentos(nome=nome, endereco=endereco, data_dia=data_dia, horario=horario)
    db.session.add(novo_agendamento)
    db.session.commit()

    arquivo = request.files['arquivo']
    upload_path = app.config['UPLOAD_PATH']
    timestamp = time.time()
    arquivo.save(f'{upload_path}/capa{novo_agendamento.id}-{timestamp}.jpg')

    return redirect(url_for('index'))

@app.route('/editar/<int:id>')
def editar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('editar', id=id)))
    agendamento = Agendamentos.query.filter_by(id=id).first()
    form = FormularioAgendamento()
    form.nome.data = agendamento.nome
    form.endereco.data = agendamento.endereco
    form.horario.data = agendamento.horario
    form.data_dia.data = agendamento.data_dia
    capa_agendamento = recupera_imagem(id)
    return render_template('editar.html', titulo='Editando Agendamento', id=id, capa_agendamento=capa_agendamento, form=form)

@app.route('/atualizar', methods=['POST',])
def atualizar():
    form = FormularioAgendamento(request.form)

    if form.validate_on_submit():
        agendamento = Agendamentos.query.filter_by(id=request.form['id']).first()
        agendamento.nome = form.nome.data
        agendamento.endereco = form.endereco.data
        agendamento.data_dia = form.data_dia.data
        agendamento.horario = form.horario.data

        db.session.add(agendamento)
        db.session.commit()

        arquivo = request.files['arquivo']
        upload_path = app.config['UPLOAD_PATH']
        timestamp = time.time()
        deleta_arquivo(id)
        arquivo.save(f'{upload_path}/capa{agendamento.id}-{timestamp}.jpg')

    return redirect(url_for('index'))

@app.route('/deletar/<int:id>')
def deletar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))

    Agendamentos.query.filter_by(id=id).delete()
    db.session.commit()
    flash('Agendamento deletado com sucesso!')

    return redirect(url_for('index'))



@app.route('/uploads/<nome_arquivo>')
def imagem(nome_arquivo):
    return send_from_directory('uploads', nome_arquivo)