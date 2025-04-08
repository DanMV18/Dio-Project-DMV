# O presente programa tem o intuito de simular um sistema bancário simples. Conta com operações de depósito, saque e extrato, sem implementar um sistema de segurança, autenticação e identificação do usuário.
menu_inicial = """

_____________Menu________________
- [1] - DEPOSITO
- [2] - SAQUE
- [3] - EXTRATO
- [4] - SAIR
_________________________________

"""
# Os parametros iniciais e limites são definidos nas variaveis a seguir fora dos ciclos de verificação dos inputs do usuário.
saldo = 0
limite = 750
extrato = ""
saques = 0
limite_saques = 4

while True:
    # Inicialmente é solicitado do usuário um input para selecionar a opção de ação desejada de acordo com o menu indicado na variável menu_inicial.
    opcao = int(input(menu_inicial))

    if opcao == 1:
        # Selecionada a opão de depósito o programa indica para o usuário a opção e solicita o valor que deseja depositar.
        print("DEPOSITO")
        deposito = float(input("DIGITE O VALOR DO DEPÓSITO DESEJADO: "))

        if deposito <= 0:
            # Verificação se o valor é válido e positivo.
            print("NÃO FOI POSSIVEL COMPLETAR A OPERAÇÃO! O VALOR DIGITADO É INVÁLIDO.")
        else:
            # Com o valor válido o programa adiciona o valor ao saldo, indica tal ação para o usuário e a adiciona ao extrato.
            saldo += deposito
            print("O VALOR FOI DEPOSITADO COM SUCESSO!")
            extrato += f"DEPOSITO: R${deposito:.2f}\n"
    elif opcao == 2:
        # Indica ao usuário que a opção SAQUE foi selecionada e solicita o valor que deseja sacar.
        print("SAQUE")
        saque = float(input("DIGITE O VALOR QUE DESEJA SACAR: "))
        if saque > limite:
            # Verifica se o valor é superior ao limite estipulado pelo banco.
            print("NÃO FOI POSSIVEL COMPLETAR A OPERAÇÃO! O VALOR EXCEDE O LIMITE DE SAQUE.")
        elif saque <= 0:
            # Verifica se o valor é válido e positivo.
            print("NÃO FOI POSSIVEL COMPLETAR A OPERAÇÃO! O VALOR DIGITADO É INVÁLIDO.")
        elif saques >= limite_saques:
            # Verifica se o usuário excedeu o número de saques estipulados pelo banco como limite.
            print("NÃO FOI POSSIVEL COMPLETAR A OPERAÇÃO! VOCÊ EXCEDEU O NÚMERO DE SAQUES PERMITIDOS NO DIA.")
        elif saque > saldo:
            # Verifica se o saque é superior ao saldo.
            print("NÃO FOI POSSIVEL COMPLETAR A OPERAÇÃO! O VALOR DIGITADO É SUPERIOR AO SALDO.")
        else:
            # Com o valor válido o progrema subtrai o valor do saldo, indica ao usuário o sucesso da ação, adiciona a ação ao extrato e adiciona contagem à variável que indica o contador a ser confrontado com o limite de saques.
            saldo -= saque
            print("O SAQUE FOI REALIZADO COM SUCESSO!")
            extrato += f"SAQUE: R${saque:.2f}\n"
            saques += 1

    elif opcao == 3:
        # A opção apresenta ao usuário o extrato de ações, demonstrando se não houve ações e, se houve, quais foram e qual é o saldo restante.
        print("""_______________EXTRATO_________________\n""")
        print("NÃO FORAM REALIZADAS MOVIMENTAÇÕES." if not extrato else extrato)
        print(f"\n\nSEU SALDO É: R${saldo:.2f}.")
        print("""_______________________________________""")

    elif opcao == 4:
        # A opção termina o programa quebrando o cicle while e apresenta a mensagem de despedida do programa.
        break

    else:
        # Apresenta ao usuário que a opção digitada não é válida de acordo com as opções do menu_inicial.
        print("A OPÇÃO DIGITADA NÃO É VALIDA! POR FAVOR ESCOLHA UMA DAS OPÇÃO APRESENTADAS NO MENU INICIAL!")

print("OBRIGADO POR UTILIZAR NOSSOS SERVIÇOS! VOLTE SEMPRE!")
