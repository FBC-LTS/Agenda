import sqlite3
from sqlite3 import Error


class Data:
    def __init__(self, file):
        self.con = sqlite3.connect(file)
        self.cur = self.con.cursor()
        print('conectado...')
        self.cur.execute('CREATE TABLE IF NOT EXISTS tb_contato('
                         'id INTEGER PRIMARY KEY AUTOINCREMENT,'
                         'num text NOT NULL,'
                         'nome text NOT NULL,'
                         'email text NOT NULL'
                         ');')

    def getAll(self):
        try:
            return self.cur.execute('SELECT * FROM tb_contato').fetchall()
        except Error as ex:
            print(ex)

    def getContato(self, elemento):
        try:
            return self.cur.execute(f'SELECT * FROM tb_contato WHERE id = {elemento}').fetchone()
        except Error as ex:
            print(ex)

    def salvarContato(self, contato):
        try:
            self.cur.execute("INSERT INTO tb_contato(num, nome, email) VALUES(?, ?, ?)", contato)
            self.con.commit()
            print('salvo')
        except Error as ex:
            print(ex)

    def apagar(self, elemento):
        try:
            self.cur.execute(f"DELETE FROM tb_contato WHERE id = {elemento}")
            self.con.commit()
            print('apagado')
        except Error as ex:
            print(ex)

    def alterarContato(self, coluna: str, valor: str, elemento: int):
        try:
            print(f'{coluna} {valor}')
            self.cur.execute(f"UPDATE tb_contato SET {coluna}= '{valor}' WHERE id = {elemento}")
            self.con.commit()
            print(f'alterado')
        except Error as ex:
            print(ex)

    def saveExit(self):
        self.con.commit()
        self.con.close()
        print('saindo...')
