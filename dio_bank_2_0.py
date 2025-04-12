import datetime

def menu():
    menu_inicial = """  

   ________BANCO DIO________

_____________Menu________________
- [1] - DEPOSITO
- [2] - SAQUE
- [3] - EXTRATO
- [4] - CRIAR NOVO USUÁRIO
- [5] - CRIAR CONTA
- [6] - LISTAR CONTAS
- [7] - SAIR
_________________________________

    """
    return menu_inicial

def criar_usuario(usuarios):
    cpf = input("DIGITE O CPF DO NOVO USUÁRIO: ")
    usuario = filtrar_usuarios(cpf, usuarios)

    if usuario:
        print("USUÁRIO JÁ CADASTRADO!")
        return

    nome = input("DIGITE O NOME DO NOVO USUÁRIO: ")
    nascimento = input("DIGITE A DATA DE NASCIMENTO DO NOVO USUÁRIO (DD/MM/AAAA): ")
    endereco = input("DIGITE O ENDEREÇO DO NOVO USUÁRIO: ")
    usuarios.append({"nome": nome, "cpf": cpf, "nascimento": nascimento, "endereco": endereco})
    print(f"USUÁRIO CRIADO COM SUCESSO!\n BEM VINDO AO BANCO DIO, {nome.upper()}!")

def criar_conta(agencia, numero_conta, usuarios, contas):
    cpf = input("DIGITE O CPF DO USUÁRIO: ")
    usuario = filtrar_usuarios(cpf, usuarios)

    if not usuario:
        print("USUÁRIO NÃO ENCONTRADO!")
        return
    
    conta = {
        "agencia": agencia,
        "numero_conta": numero_conta,
        "usuario": usuario,
        "saldo": 0,  
        "extrato": ""  
    }
    contas.append(conta)
    print(f"CONTA CRIADA COM SUCESSO! SUA CONTA É: {numero_conta} E SUA AGENCIA É: {agencia}.")
    print(f"BEM VINDO AO BANCO DIO, {usuario['nome'].upper()}!")

def buscar_conta(numero_conta, contas):
    for conta in contas:
        if conta["numero_conta"] == numero_conta:
            return conta
    return None

def deposito_conta(numero_conta, contas, valor):
    conta = buscar_conta(numero_conta, contas)
    if not conta:
        print("CONTA NÃO ENCONTRADA!")
        return

    if valor <= 0:
        print("NÃO FOI POSSIVEL COMPLETAR A OPERAÇÃO! O VALOR DIGITADO É INVÁLIDO.")
    else:
        data = datetime.datetime.now()
        data_formatada = data.strftime("%d/%m/%Y %H:%M")
        conta["saldo"] += valor
        conta["extrato"] += f"DEPOSITO: R${valor:.2f}, {data_formatada}\n"
        print("O VALOR FOI DEPOSITADO COM SUCESSO!")

def saque_conta(numero_conta, contas, valor, limite, limite_saques):
    conta = buscar_conta(numero_conta, contas)
    if not conta:
        print("CONTA NÃO ENCONTRADA!")
        return

    if valor > limite:
        print("NÃO FOI POSSIVEL COMPLETAR A OPERAÇÃO! O VALOR EXCEDE O LIMITE DE SAQUE.")
    elif valor <= 0:
        print("NÃO FOI POSSIVEL COMPLETAR A OPERAÇÃO! O VALOR DIGITADO É INVÁLIDO.")
    elif conta.get("saques", 0) >= limite_saques:
        print("NÃO FOI POSSIVEL COMPLETAR A OPERAÇÃO! VOCÊ EXCEDEU O NÚMERO DE SAQUES PERMITIDOS NO DIA.")
    elif valor > conta["saldo"]:
        print("NÃO FOI POSSIVEL COMPLETAR A OPERAÇÃO! O VALOR DIGITADO É SUPERIOR AO SALDO.")
    else:
        data = datetime.datetime.now()
        data_formatada = data.strftime("%d/%m/%Y %H:%M")
        conta["saldo"] -= valor
        conta["extrato"] += f"SAQUE: R${valor:.2f}, {data_formatada}\n"
        conta["saques"] = conta.get("saques", 0) + 1
        print("O SAQUE FOI REALIZADO COM SUCESSO!")

def extrato_conta(numero_conta, contas):
    conta = buscar_conta(numero_conta, contas)
    if not conta:
        print("CONTA NÃO ENCONTRADA!")
        return
    data = datetime.datetime.now()
    data_formatada = data.strftime("%d/%m/%Y %H:%M")
    print("""_______________EXTRATO_________________\n""")
    print("NÃO FORAM REALIZADAS MOVIMENTAÇÕES." if not conta["extrato"] else conta["extrato"])
    print(f"\n\nSEU SALDO É: R${conta['saldo']:.2f}, {data_formatada}.")
    print("""_______________________________________""")

def listar_contas(contas):
    for conta in contas:
        print(f"AGÊNCIA: {conta['agencia']}, CONTA: {conta['numero_conta']}, USUÁRIO: {conta['usuario']['nome']}")

def filtrar_usuarios(cpf, usuarios):
    for usuario in usuarios:
        if usuario["cpf"] == cpf:
            return usuario
    return None

def main():
    menu_inicial = menu()
    usuarios = []
    contas = []
    numero_conta = 1
    limite = 500
    limite_saques = 3

    while True:
        opcao = int(input(menu_inicial))

        if opcao == 1:
            print("DEPOSITO")
            numero = int(input("DIGITE O NÚMERO DA CONTA: "))
            valor = float(input("DIGITE O VALOR DO DEPÓSITO DESEJADO: "))
            deposito_conta(numero, contas, valor)

        elif opcao == 2:
            print("SAQUE")
            numero = int(input("DIGITE O NÚMERO DA CONTA: "))
            valor = float(input("DIGITE O VALOR QUE DESEJA SACAR: "))
            saque_conta(numero, contas, valor, limite, limite_saques)

        elif opcao == 3:
            print("EXTRATO")
            numero = int(input("DIGITE O NÚMERO DA CONTA: "))
            extrato_conta(numero, contas)

        elif opcao == 4:
            criar_usuario(usuarios)

        elif opcao == 5:
            criar_conta(agencia="0001", numero_conta=numero_conta, usuarios=usuarios, contas=contas)
            numero_conta += 1

        elif opcao == 6:
            listar_contas(contas)

        elif opcao == 7:
            print("OBRIGADO POR UTILIZAR O BANCO DIO!")
            break

        else:
            print("A OPÇÃO DIGITADA NÃO É VALIDA! POR FAVOR ESCOLHA UMA DAS OPÇÃO APRESENTADAS NO MENU INICIAL!")

main()