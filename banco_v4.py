#Adicionar Classes para cliente e as operacoes bancarias: deposito e saque
from abc import ABC
from datetime import datetime

class Cliente:
    def __init__(self, endereco) -> None:
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, cpf, nome:str, data_nasc, endereco) -> None:
        super().__init__(endereco)
        self._cpf = cpf
        self._nome = nome
        self._data_nasc = data_nasc      

    @property
    def cpf(self):
        return self._cpf                                                                                                                                                 

class Conta:
    def __init__(self,cliente, numero) -> None:
        self._saldo = 0
        self._numero = numero
        self._agencia = '0001'
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente:Cliente, numero:int): # -> Conta
        return cls(numero, cliente)

    # def nova_conta(self, cliente:Cliente, numero:int):
    #     self._cliente = cliente
    #     self._numero = numero

    @property
    def numero(self):
        return self._numero
    
    @property
    def agencia(self):
        return self._agencia

    @property
    def saldo(self) -> float:
        return self._saldo

    @property
    def historico(self):
        return self._historico
    
    @property
    def cliente(self):
        return self._cliente

    def sacar(self, valor:float) -> bool:
        excedeu_saldo = valor > self._saldo
        
        if excedeu_saldo:
            print('Saldo insuficiente')
            return False
        else:
            self._saldo -= valor
            return True
    
    def depositar(self, valor) -> bool:
        if valor > 0:
            self._saldo += valor
            return True
        return False


class ContaCorrente(Conta):
    def __init__(self, cliente, numero, limite=500, limite_saques=3) -> None:
        super().__init__(numero, cliente)
        self._limite = limite
        self.limite_saques = limite_saques
    
    def sacar(self, valor:float) -> bool:
        transacoes = self.historico.transacoes
        saques_realizados = 0
        for transacao in transacoes:
            if transacao['tipo'] == 'Saque':
                saques_realizados += 1

        excedeu_saldo = valor > self._saldo
        excedeu_limite = valor > 500
        excedeu_limite_saques = saques_realizados > self.limite_saques

        if excedeu_saldo:
            print('Saldo insuficiente.')
            return False
        elif excedeu_limite:
            print(f'Voce ultrapassou o limite de R${self._limite}')
            return False
        elif excedeu_limite_saques:
            print('Voce atingiu o limite de saques diarios.')
            return False
        else:
            self._saldo -= valor
            return True
        
    def __str__(self) -> str:
        return f"Titular {self.cliente._nome} - Conta {self._numero} - Agência {self.agencia} - Saldo: R${self.saldo:.2f}"

class Historico():
    def __init__(self) -> None:
        self._historico = []

    @property
    def transacoes(self):
        return self._historico

    def adicionar_transacao(self, transacao):
        data = return_data()
        self._historico.append({
            "tipo": transacao.__class__.__name__,
            "valor": transacao._valor,
            "data": data
            }
        )

class Transacao(ABC):
    def registrar(self, conta:Conta):
        pass

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    def registrar(self, conta:Conta):
        transacao = conta.depositar(self._valor) #REALIZAR A OPERACAO E VERIFICAR SE OCORREU TUDO CERTO E EXIBIR UMA MENSAGEM

        if transacao:
            conta.historico.adicionar_transacao(self)
            print('DEPOSITO REALIZADO COM SUCESSO.')
            return
    
class Saque(Transacao):
    def __init__(self, valor) -> None:
        self._valor = valor
    
    def registrar(self, conta:Conta):
        transacao = conta.sacar(self._valor)

        if transacao:
            conta.historico.adicionar_transacao(self)
            print('Saque realizado com sucesso')
        
        return 'Ocorreu um erro na operacao. Tente novamente.'
    
def return_data():
    data = datetime.now()
    data = data.strftime('%d/%m/%Y %H:%M:%S')
    return data


def recuperar_conta_cliente(cliente):
    if cliente.contas:
        return cliente.contas[0]
    return False

def depositar(clientes:Cliente):
    cpf = input('Digite o CPF do titular da conta para realizar o deposito: ')
    cliente = usuario_existe(clientes, cpf)
    if not cliente:
        print('Usuario nao encontrado.')
        return

    valor = float(input('Informe um valor para deposito: '))
    transacao = Deposito(valor)
    conta = recuperar_conta_cliente(cliente)
    cliente.realizar_transacao(conta, transacao)

def sacar(clientes):
    cpf = input('Digite o CPF do titular da conta para realizar o saque: ')
    cliente = usuario_existe(clientes, cpf)
    if not cliente:
        print('Usuario nao encontrado')
        return

    valor = float(input('Informe o valor para saque: '))
    transacao = Saque(valor)
    conta = recuperar_conta_cliente(cliente)
    cliente.realizar_transacao(conta, transacao)
    

def usuario_existe(clientes:Cliente, cpf):
    if not clientes:
        return False
    
    for cliente in clientes:
        if cliente.cpf == cpf:
            return cliente
        
    return False

def extrato(clientes):
    cpf = input('Digite o CPF: ')
    cliente = usuario_existe(clientes, cpf)
    if not cliente:
        print('Voce nao esta cadastrado.')
        return
    
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        print('Voce nao tem uma conta vinculada ao seu usuario.')
        return
    elif not conta.historico.transacoes:
        print('Nao foram realizadas movimentacões')
        return

    for transacao in conta.historico.transacoes:
        print(f'{transacao['tipo']} - {transacao['valor']:.2f} - {transacao['data']}')

def listar_contas(contas):
    for conta in contas:
        print(conta)

def criar_usuario(clientes:list):
    cpf = input('Digite seu CPF: (APENAS NUMEROS) ')
    if usuario_existe(clientes, cpf):
        print('Usuario ja cadastrado')
        return
    
    nome = input('Digite seu nome: ')
    data_nasc = input('Digite sua data de nascimento: dd/mm/aaaa ')
    endereco = input('Digite seu endereco: ')

    clientes.append(PessoaFisica(cpf, nome, data_nasc, endereco))
    print('Usuario cadastrado com sucesso.')
    return


def criar_conta(clientes:Cliente, contas, num_conta):
    cpf = input('Digite o CPF do titular da conta:')
    cliente = usuario_existe(clientes, cpf)
    if cliente:
        conta = ContaCorrente.nova_conta(cliente, num_conta)
        cliente.adicionar_conta(conta)
        contas.append(conta)
    else:
        print('Usuario nao encontrado')
    
    print('@@@ CONTA CRIADA COM SUCESSO @@@')
    return

menu = """

[NU] Novo Usuario 
[NC] Nova Conta 
[D] Deposito 
[S] Saque 
[E] Extrato 
[LC] Listar Contas
[Q] Sair 
=> """

num_conta = 1
clientes = []
contas = []

while True:
    print('='*25, 'MENU', '='*25)
    opcao = input(menu).lower()
    print('\n')
    if opcao == 'nu':
        # clientes = criar_usuario(clientes)
        criar_usuario(clientes)
    elif opcao == 'nc':
        # contas = criar_conta(clientes, contas, num_conta)
        criar_conta(clientes, contas, num_conta)
        num_conta += 1
    elif opcao == "d":
        depositar(clientes)
    elif opcao == "s":
        sacar(clientes)
    elif opcao == "e":
        extrato(clientes)
    elif opcao == 'lc':
        listar_contas(contas)
    elif opcao == "q":
        break
    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")
    