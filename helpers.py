import os
from coletaon import app
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, validators

class FormularioAgendamento(FlaskForm):
    nome = StringField('Nome do Solicitante', [validators.DataRequired(), validators.Length(min=1, max=100)])
    endereco = StringField('Endereço', [validators.DataRequired(), validators.Length(min=1, max=150)])
    data_dia = StringField('Data', [validators.DataRequired(), validators.Length(min=1, max=10)])
    horario = StringField('Horário', [validators.DataRequired(), validators.Length(min=1, max=5)])
    salvar = SubmitField('Salvar')

class FormularioUsuario(FlaskForm):
    nickname = StringField('Nickname', [validators.DataRequired(), validators.Length(min=1, max=8)])
    senha = PasswordField('Senha', [validators.DataRequired(), validators.Length(min=1, max=100)])
    login = SubmitField('Login')

def recupera_imagem(id):
    for nome_arquivo in os.listdir(app.config['UPLOAD_PATH']):
        if f'capa{id}' in nome_arquivo:
            return nome_arquivo

    return 'capa_padrao.jpg'

def deleta_arquivo(id):
    arquivo = recupera_imagem(id)
    if arquivo != 'capa_padrao.jpg':
        os.remove(os.path.join(app.config['UPLOAD_PATH']), arquivo)