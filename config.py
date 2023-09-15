import os

SECRET_KEY = 'alura'

SQLALCHEMY_DATABASE_URI = \
    '{SGBD}://{usuario}:{senha}@{servidor}/{database}?auth_plugin=mysql_native_password'.format(
        SGBD = 'mysql+mysqlconnector',
        usuario = 'root',
        senha = 'alvorada',
        servidor = 'localhost',
        database = 'coletaon'
    )

UPLOAD_PATH = os.path.dirname(os.path.abspath(__file__)) + '/uploads'