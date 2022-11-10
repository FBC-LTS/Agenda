from time import sleep

import DATA
import re

stdarrow = "\n >>> "
sep = '-=-' * 10


class App:
    def __init__(self):
        self.data = DATA.Data('contato.db')
        self.contatos = []

    def start(self):
        print('Ola eu sou seu gerenciador de contatos.')
        print('(fora do menu: digite 0 para voltar ao menu)')
        self.opcaoUser()

    def cenario(self, escolha):
        match escolha:
            case 0:
                print(f'\n{sep}\nescolheu 0\n')
                self.exit()
            case 1:
                print(f'\n{sep}\nescolheu 1\n')
                self.criarContato()
            case 2:
                print(f'\n{sep}\nescolheu 2\n')
                self.visualizarContatos()
            case 3:
                print(f'\n{sep}\nescolheu 3\n')
                self.apagarContatos()
            case 206:
                print("Deseja sair?(alterações podem não estar salvas)[0: continuar || 1: sair]")
                escolha = int(input(stdarrow))
                if (escolha):
                    self.exit()
                else:
                    self.opcaoUser()
            case _:
                self.opcaoUser()

    def opcaoUser(self):
        escolha = ''
        try:
            print(f'{sep}'
                  '\n|     Menu Principal     |'
                  '\n|    DIGITE UMA OPÇAO:   |'
                  '\n| 1 : criar contato      |'
                  '\n| 2 : visualizar contatos|'
                  '\n| 3 : apagar contato     |'
                  '\n| 0 : sair               |\n')
            escolha = int(input(stdarrow))
        except:
            print("valor invalido")
            self.opcaoUser()
        self.cenario(escolha)

    def visualizarContatos(self):
        self.contatos = self.data.getContatos()
        print("| ID | Telefone | Nome | e-mail |")
        for contato in self.contatos:
            print(f"|{contato[0]} | {contato[1]} | {contato[2]} | {contato[3]} |")
        sleep(2)
        self.opcaoUser()

    def escolhaContato(self):
        print('Aperte enter para continuar!')
        print('Ou digite: "S" para salvar e sair')
        escolha = input(stdarrow).upper()
        self.tixe(escolha)
        match escolha:
            case "S":
                self.opcaoUser()
            case _:
                self.criarContato()

    def criarContato(self):
        contato = {"num": '', "nome": '', "email": ''}
        self.pegaContato(contato)
        escolha = input(stdarrow)
        self.tixe(escolha)
        contato = list(contato.values())
        self.data.salvarContato(contato)
        self.opcaoUser()

    def pegaContato(self, contexto):
        print('Digite o nome do novo contato:')
        contexto["nome"] = input(stdarrow).capitalize()
        if contexto["nome"].replace(' ', '') == '':
            return self.pegaContato(contexto)
        return self.pegaNumero(contexto)

    def pegaNumero(self, contexto):
        print('Digite o Numero com 11(ddd+num) digitos:\n(Ou formato padrão ex: (55)99123-4567.)')
        num = input(stdarrow)

        if len(num) == 11 and num.isnumeric():
            contexto["num"] = f'({num[0:2]}){num[1:6]}-{num[7:11]}'
            return self.pegaEmail(contexto)
        elif re.fullmatch(r'^\([1-9]{2}\)[0-9]{5}\-[0-9]{4}$', num):
            contexto["num"] = num
            return self.pegaEmail(contexto)
        return self.pegaNumero(contexto)

    def pegaEmail(self, contexto):
        print(f'Digite o email do contato:')
        contexto["email"] = input(stdarrow)
        if not re.fullmatch(r'^[a-zA-Z0-9]+(?:\.[a-zA-Z0-9]+)*@[a-zA-Z0-9]+(?:\.[a-zA-Z0-9]+)*$+', contexto["email"]):
            print("Invalid Email")
            self.pegaEmail(contexto)

    def apagarContatos(self):
        print("Qual o ID do contato que deseja apagar?"
              "\n(caso deseje cancelar digite um letra)")
        ind = int(input(stdarrow))
        self.tixe(ind)
        target = self.data.getContato(ind)
        if target:
            print('Deseja apagar:')
            for dado in target:
                print(f'| {dado} |', end='')
            print('\nS: sim | N: não')
            apagar = input(stdarrow).upper()
            apagar = apagar == "S"
            if apagar:
                self.data.apagarIndex(ind)
                print("\napagando")
                return self.opcaoUser()
        print("\nnao foi apagado")
        return self.opcaoUser()

    def exit(self):
        self.data.saveExit()

    def tixe(self, valor):
        if valor == 0:
            self.opcaoUser()

