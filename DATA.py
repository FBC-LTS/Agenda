import sqlite3


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

    def getContatos(self):
        return self.cur.execute('SELECT * FROM tb_contato').fetchall()

    def getContato(self, idContato):
        return self.cur.execute(f'SELECT * FROM tb_contato WHERE id = {idContato}').fetchone()

    def salvarContato(self, contato):
        self.cur.execute("INSERT INTO tb_contato(num, nome, email) VALUES(?, ?, ?)", contato)
        self.con.commit()
        print('salvo')

    def salvarContatos(self, contatos):
        self.cur.executemany("INSERT INTO tb_contato(num, nome, email) VALUES(?, ?, ?)", contatos)
        self.con.commit()
        print('salvo')

    def apagarIndex(self, idC):
        self.cur.execute(f"DELETE FROM tb_contato WHERE id = {str(idC)}")
        self.con.commit()

    def saveExit(self):
        self.con.commit()
        self.con.close()
        print('saindo...')

