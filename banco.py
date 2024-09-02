# Todos os depositos devem ser armazenador em uma variavel e exibidos na operacao de extrato
# Limite de 3 SAQUES DIARIOS LIMITE DE R$500
# Se o usuario nao tiver saldo exibir uma mensagem informando que nao sera possivel sacar

menu = """
[S] SACAR
[D] DEPOSITAR
[E] EXTRATO
[Q] SAIR
> > > """
limite = 500
LIMITE_SAQUES = 3
extrato = list()
saldo = 0
numero_saques = 0

while True:
    print('='*40)
    opcao = input(menu).lower()

    if opcao == 's':
        valor = float(input('Quanto deseja sacar: '))

        if valor > limite:
            print(f'Valor ultrapassou o limite de R${limite}')\
        
        elif valor > saldo:
            print('Saldo Insuficiente')
            
        elif numero_saques >= LIMITE_SAQUES:
            print('Numero maximo de saques excedido')
        
        elif valor < 0:
            print('Valor informado e invalido.')
        
        else:
            saldo -= valor
            numero_saques += 1
            print(f'Voce realizou um saque de R${valor:.2f} seu saldo agora é de R${saldo:.2f}')
            extrato.append(f'SAQUE: R${valor:.2f}')
            

    elif opcao == 'd':
        valor = float(input('Quanto deseja depositar: '))

        if valor > 0:
            saldo += valor
            extrato.append(f'DEPOSITO: R${valor:.2f}')
            print(f'Deposito realizado com sucesso, seu saldo agora é de R${saldo:.2f}')
        else:
            print('Nao foi possivel realizar o deposito')
            
    elif opcao == 'e':
        print('=============== EXTRATO ===============')
        if not extrato:
            print('Nao a nenhuma operacao para ser exibida.')
            continue

        for operacao in extrato:
            print(operacao)
        print('\n')
        print(f'Saldo: R${saldo:.2f}')
        
    
    elif opcao == 'q':
        print('Saindo do sistema...')
        break
    
    else:
        print('Digite uma opcao valida')

