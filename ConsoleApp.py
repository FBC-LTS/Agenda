from time import sleep
import DATA
import re

stdarrow = "\n >>> "
sep = '-=-' * 10


class App:
    def __init__(self):
        self.data = DATA.Data('contato.db')
        self.contatos = []
        self.__updateList()

    def __updateList(self):
        self.contatos = self.data.getAll()

    def __opcaoUser(self):
        print(f'{sep}'
              '\n|     Menu Principal     |'
              '\n|    DIGITE UMA OPÇAO:   |'
              '\n| 1 : criar contato      |'
              '\n| 2 : visualizar contatos|'
              '\n| 3 : apagar contato     |'
              '\n| 4 : mudar contato      |'
              '\n| 0 : sair               |\n')
        escolha = int(input(stdarrow))
        self.__menu(escolha)

    def __menu(self, escolha):
        match escolha:
            case 0:
                print(f'\n{sep}\nescolheu 0\n')
                self.__exit()
            case 1:
                print(f'\n{sep}\nescolheu 1\n')
                self.__criarContato()
            case 2:
                print(f'\n{sep}\nescolheu 2\n')
                self.__visualizarContatos()
            case 3:
                print(f'\n{sep}\nescolheu 3\n')
                self.__apagarContatos()
            case 4:
                print(f'\n{sep}\nescolheu 4\n')
                self.__alterarContato()
            case _:
                return 404

    def __criarContato(self):
        contato = []
        print('Criando contato\n digite 0 voltar menu')
        contato.append(self.__pegaContato())
        self.__back(input(stdarrow))
        contato.append(self.__pegaNumero())
        self.__back(input(stdarrow))
        contato.append(self.__pegaEmail())
        self.data.salvarContato(contato)
        self.__updateList()
        self.__opcaoUser()

    def __pegaContato(self):
        print('Digite o nome do contato:')
        contato = input(stdarrow).lower()
        self.__back(contato)
        if contato.replace(' ', '') == '':
            self.__pegaContato()
        return contato

    def __pegaNumero(self):
        print('Digite o Numero com 11(ddd+num) digitos:\n(Ou formato padrão ex: (55)99123-4567.)')
        num = input(stdarrow)
        self.__back(num)
        if len(num) == 11 and num.isnumeric():
            return f'({num[0:2]}){num[1:6]}-{num[7:11]}'
        elif re.fullmatch(r'^\([1-9]{2}\)[0-9]{5}-[0-9]{4}$', num):
            return num
        self.__pegaNumero()

    def __pegaEmail(self):
        print('Digite o email do contato:')
        escolha = input(stdarrow)
        self.__back(escolha)
        if not re.fullmatch(r'^[a-zA-Z0-9]+(?:\.[a-zA-Z0-9]+)*@[a-zA-Z0-9]+(?:\.[a-zA-Z0-9]+)*$+',
                            escolha):
            print("Invalid Email")
            self.__pegaEmail()
        return escolha

    def __visualizarContatos(self):
        print("| ID | Telefone | Nome | e-mail |")
        for contato in self.contatos:
            print(f"|{contato[0]} | {contato[1]} | {contato[2]} | {contato[3]} |")
        sleep(2)
        self.__opcaoUser()

    def __apagarContatos(self):
        print("Qual o ID do contato que deseja apagar?"
              "\n(caso deseje cancelar digite um letra)")
        ind = int(input(stdarrow))
        self.__back(ind)
        target = self.data.getContato(ind)
        if target:
            print('Deseja apagar:')
            print(f'{target[1]} {target[2]} {target[3]}')
            print('\nS: sim | N: não')
            apagar = input(stdarrow).upper().strip()
            if apagar == "S" or apagar == "SIM":
                print("\n Apagando.")
                self.data.apagar(ind)
                self.__updateList()
                self.__opcaoUser()

        print("\nnao foi apagado")
        self.__opcaoUser()

    def __colunaBuscas(self):
        print('Deseja buscar por nome ou por id?\nDigite "nome" ou "id"')
        coluna = input(stdarrow).lower().strip()
        self.__back(coluna)
        match coluna:
            case "nome":
                return coluna
            case "id":
                return coluna
            case _:
                self.__colunaBuscas()

    def __idElemento(self, coluna) -> int:
        print(f'Digite o {coluna} dele:')
        elemento = input(stdarrow)
        match coluna:
            case "nome":
                valorId = -1
                for contato in self.contatos:
                    if contato[2].lower() == elemento.lower().strip():
                        valorId = contato[0]
                if valorId >= 0:
                    return valorId
            case "id":
                if elemento.isnumeric():
                    return int(elemento)
        self.__idElemento(coluna)

    def __menuColuna(self) -> list:
        print("O que deseja alterar?\n 'nome', 'numero', 'email'")
        escolha = input(stdarrow).lower().strip()
        match escolha:
            case 'nome':
                valor = str(self.__pegaContato())
                return ['nome', valor]
            case 'num', 'numero':
                valor = str(self.__pegaNumero())
                return ['num', valor]
            case 'email', 'e-mail', 'mail':
                valor = str(self.__pegaEmail())
                return ['email', valor]
            case _:
                self.__menuColuna()

    def __alterarContato(self):
        coluna = self.__colunaBuscas()
        valorId = self.__idElemento(coluna)
        par = self.__menuColuna()
        self.data.alterarContato(par[0], par[1], valorId)

    def __exit(self):
        self.data.saveExit()

    def __back(self, valor):
        if valor == 0 or valor == '0':
            self.__opcaoUser()

    def start(self):
        print('Ola eu sou seu gerenciador de contatos.')
        self.__opcaoUser()
