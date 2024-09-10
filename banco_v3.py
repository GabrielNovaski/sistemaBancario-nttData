#SAQUE - A funcao deve receber os argumentos apenas por nome (keyword only)
# Sugestao de argumentos: Saldo, valor, extrato, limite, numero_saques, limite_saques.
#Return saldo e extrato

#DEPOSITO (Positional Only)- saldo, valor extrato 
# Return saldo e extrato

#EXTRATO (Positional = saldo e Keyword = extrato) - 

#CRIAR USARIO - armazenar os usuarios em uma lista, 
# um usuario composto por: nome,data_nasc, cpf e endereco Endereco e uma string com o formato: logradouro, nmro - bairro - cidade-sigla estado
# Deve ser armazenado somente os numeros do CPF. nAO PODEMOS CADASTRAR 2 USUARIOS COM O MESMO CPF

#CRIAR CONTA - O programa deve armazenar contas em uma lista, uma conta corrente e composta por: agencia, numero da conta, usuario
#O nmero da conta e sequencial iniciando em 1. O numero da agencia e fixo: "0001". o Usuario pode ter mais de uma conta, mas uma conta pertence a somente um usuario

def sacar(*, saldo, valor, extrato:list):
    saldo -= valor
    extrato.append(f'SAQUE: R${valor:.2f}')
    print(f'SAQUE REALIZADO NO VALOR DE R${valor:.2f} SEU SALDO AGORA E DE R${saldo:.2f}.')
    return saldo, extrato

def deposito(saldo, valor, extrato,/):
    print("=== DEPOSITO REALIZADO COM SUCESOS! ===")
    extrato.append(f"DEPOSITO: R${valor:.2f}")
    saldo += valor
    return saldo, extrato

def mostrar_extrato(extrato, saldo):
    if not extrato:
        print('@@@   VOCE NAO FEZ NENHUMA OPERACAO   @@@')
        return
    
    print('='*55)
    for op in extrato:
        print(op)

    print('\n')
    print(f'SEU SALDO É DE R${saldo:.2f}')

def usuario_existe(usuarios, cpf):
    if not usuarios:
        return False
    
    for usuario in usuarios:  
        if cpf == usuario['cpf']:
            return True
        
    return False

def validar_saque(valor, saldo, num_saques, limite=500, limite_saques=3) -> bool:
    excedeu_saldo = valor > saldo  # VERIFICA SE O CLIENTE TEM O VALOR PARA SER SACADO
    excedeu_limite = valor > limite # VERIFICA SE NAO ULTRAPASSOU O LIMITE DO SAQUE
    excedeu_saques = num_saques >= limite_saques # VERIFICA SE NAO PASSOU O LIMITE DE SAQUES DIARIOS

    if excedeu_saldo:
        print('Saldo insuficiente.')
        return False
    elif excedeu_limite:
        print(f'O valor excedeu o limite de R${limite}')
        return False
    elif excedeu_saques:
        print('Voce excedeu o limite de saques diarios.')
        return False
    else:
        return True

def criar_usuario(cpf):
    nome = input('Digite seu nome: ')
    endereco = input('Digite seu endereco: ')
    data_nasc = input('Data de Nascimento dd/mm/aaaa ')

    return {'nome': nome, 'endereco': endereco, 'cpf': cpf, 'data_nasc': data_nasc}

def criar_conta(cpf, usuarios, num_conta, AGENCIA):
    for usuario in usuarios:
        if usuario['cpf'] == cpf:
            usuario_adicionar = {'agencia': AGENCIA, 'num_conta': num_conta, 'usuario': usuario}
            print('CONTA CRIADA COM SUCESSO')
            return usuario_adicionar

def listar_contas(contas):
    if not contas:
        print('NENHUMA CONTA ESTA CADASTRADA')

    for conta in contas:
        print(f"AGENCIA:{'':<10} {conta['agencia']}")
        print(f"C/C:{'':<14} {conta['num_conta']}")
        print(f"TITULAR:{'':<10} {conta['usuario']['nome']}\n")

menu = """

[NU] Novo Usuario 
[NC] Nova Conta 
[D] Deposito 
[S] Saque 
[E] Extrato 
[LC] Listar Contas
[Q] Sair 
=> """
LIMITE_SAQUES = 3
AGENCIA = '0001'

saldo = 0
limite = 500
extrato = []
numero_saques = 0
usuarios = []
contas = []
num_conta = 1
while True:
    print('='*25, 'MENU', '='*25)
    opcao = input(menu).lower()
    print('\n')
    if opcao == 'nu':
        cpf = input('Digite o cpf: (SOMENTE NUMEROS) ')
        if usuario_existe(usuarios, cpf):
            print('ESTE USUARIO JA ESTA CADASTRADO.')
            continue

        usuarios.append(criar_usuario(cpf))
        print('\n@@@ USUARIO CADASTRADO COM SUCESSO @@@')

    elif opcao == 'nc':
        cpf = input('Insira seu cpf: ')
        if usuario_existe(usuarios, cpf):
            contas.append(criar_conta(cpf, usuarios, num_conta, AGENCIA))
            num_conta += 1
            print("\nUSUARIO CADASTRADO COM SUCESSO")
        else:
            print('\nUSUARIO NAO ENCONTRADO. ANTES DE ABRIR UMA CONTA VOCE PRECISA SE CADASTRAR.')

    elif opcao == "d":
        valor = float(input("Informe o valor do depósito: "))

        if valor > 0:
            saldo, extrato = deposito(saldo, valor, extrato)
        else:
            print("Operação falhou! O valor informado é inválido.")

    elif opcao == "s":
        valor = float(input("Informe o valor do saque: "))
        if validar_saque(valor, saldo, numero_saques):
            saldo, extrato = sacar(saldo=saldo, valor=valor, extrato=extrato)
            numero_saques +=1

    elif opcao == "e":
        mostrar_extrato(extrato, saldo)

    elif opcao == 'lc':
        listar_contas(contas)
    
    elif opcao == "q":
        break
    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")
    