import mysql.connector
from mysql.connector import errorcode
import pymysql
from flask_bcrypt import generate_password_hash

print("Conectando...")
try:
      conn = pymysql.connect(
            host='localhost',
            user='root',
            password='alvorada'
            
      )
except pymysql.connector.Error as err:
      if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print('Existe algo errado no nome de usuário ou senha')
      else:
            print(err)

cursor = conn.cursor()

cursor.execute("DROP DATABASE IF EXISTS `coletaon`;")

cursor.execute("CREATE DATABASE `coletaon`;")

cursor.execute("USE `coletaon`;")

# criando tabelas
TABLES = {}
TABLES['Agendamentos'] = ('''
      CREATE TABLE `agendamentos` (
      `id` int(11) NOT NULL AUTO_INCREMENT,
      `nome` varchar(100) NOT NULL,
      `endereco` varchar(150) NOT NULL,
      `data_dia` varchar(10) NOT NULL,
      `horario` varchar(5) NOT NULL,
      PRIMARY KEY (`id`)
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

TABLES['Usuarios'] = ('''
      CREATE TABLE `usuarios` (
      `nome` varchar(20) NOT NULL,
      `nickname` varchar(8) NOT NULL,
      `senha` varchar(100) NOT NULL,
      PRIMARY KEY (`nickname`)
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

for tabela_nome in TABLES:
      tabela_sql = TABLES[tabela_nome]
      try:
            print('Criando tabela {}:'.format(tabela_nome), end=' ')
            cursor.execute(tabela_sql)
      except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                  print('Já existe')
            else:
                  print(err.msg)
      else:
            print('OK')


# inserindo usuarios
usuario_sql = 'INSERT INTO usuarios (nome, nickname, senha) VALUES (%s, %s, %s)'
usuarios = [
      ("Maycon", "Maycon", generate_password_hash("123456").decode('utf-8')),
      ("Usuario1", "Usuario1", generate_password_hash("usuario1").decode('utf-8')),
      ("Usuario2", "Usuario2", generate_password_hash("usuario2").decode('utf-8'))
]
cursor.executemany(usuario_sql, usuarios)

cursor.execute('select * from coletaon.usuarios')
print(' -------------  Usuários:  -------------')

for user in cursor.fetchall():
    print(user[1])

# inserindo jogos
agendamentos_sql = 'INSERT INTO agendamentos (nome, endereco, data_dia, horario) VALUES (%s, %s, %s, %s)'
agendamentos = [
      ('Dennis Hauger', 'Avenida Presidente Tancredo de Almeida Neves, 14b', '30/08/2023', '10:00'),
      ('Jehan Daruvala', 'Rua Coronel Fagundes, 1.876', '15/08/2023', '09:30'),
      ('Zane Maloney', 'Rua Pietro Petri, 10', '01/09/2023', '14:00'),
      ('Théo Pourchaire', 'Rua Pio XII, 876', '10/09/2023', '8:00'),
      ('Enzo Fittipaldi', 'Rua XV de Novembro, 60', '25/08/2023', '12:30'),
      ('Frederik Vesti', 'Travessa 140', '05/09/2023', '16:00'),
]

cursor.executemany(agendamentos_sql, agendamentos)

cursor.execute('select * from coletaon.agendamentos')
print(' -------------  Agendamentos:  -------------')

for agendamento in cursor.fetchall():
    print(agendamento[1])

# commitando se não nada tem efeito
conn.commit()

cursor.close()
conn.close()
