from datetime import datetime
import abc
import textwrap

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)
    
class PessoaFisica(Cliente):
    def __init__(self, nome, cpf, endereco, data_nascimento):
        super().__init__(endereco)
        self.nome = nome
        self.cpf = cpf
        self.data_nascimento = data_nascimento
       
class Conta:
    def __init__(self, numero, cliente):
        self._numero = numero
        self._cliente = cliente
        self._agencia = "0001"
        self._saldo = 0
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, numero, cliente):
        return cls(numero, cliente)
    
    @property
    def saldo(self):
        return self._saldo
    
    @property
    def numero(self):
        return self._numero
    
    @property
    def agencia(self):  
        return self._agencia
    
    @property
    def cliente(self):
        return self._cliente
    
    @property
    def historico(self):
        return self._historico
    
    def sacar(self, valor):
       saldo = self._saldo
       excedeu_saldo = valor > self._saldo
       excedeu_limite = valor > self.limite
       if excedeu_saldo:
          print("\n====OPERAÇÃO FALHOU! VOCÊ NÃO TEM SALDO SUFICIENTE!====")
       elif excedeu_limite:
          print("\n====OPERAÇÃO FALHOU! O VALOR DIGITADO É MAIOR QUE O LIMITE DE SAQUE!====")
       elif valor > 0:
          self._saldo -= valor
          print(f"\n====SAQUE DE R$ {valor:.2f} REALIZADO COM SUCESSO!====")
          return True
       else:
          print("\n====OPERAÇÃO FALHOU! O VALOR INFORMADO É INVÁLIDO!====")
          return False
       

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print(f"\n====DEPÓSITO DE R$ {valor:.2f} REALIZADO COM SUCESSO!====")
            return True
        else:
            print("\n====OPERAÇÃO FALHOU! O VALOR INFORMADO É INVÁLIDO!====")
            return False
  
class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques
        self.nro_saque = 0 

    def sacar(self, valor):
        excedeu_limite = valor > self.limite
        excedeu_saques = self.nro_saque >= self.limite_saques

        if excedeu_limite:
            print("\n====OPERAÇÃO FALHOU! O VALOR DIGITADO É MAIOR QUE O LIMITE DE SAQUE!====")
        elif excedeu_saques:
            print("\n====OPERAÇÃO FALHOU! VOCÊ EXCEDEU O NÚMERO DE SAQUES PERMITIDOS!====")
        elif valor > 0:
            sucesso = super().sacar(valor)
            if sucesso:
                self.nro_saque += 1  
            return sucesso
        else:
            print("\n====OPERAÇÃO FALHOU! O VALOR INFORMADO É INVÁLIDO!====")
        return False
    
    def __str__(self):
        return f"""\
        Agência:\t{self.agencia} 
        C/C:\t\t{self.numero}
        Titular:\t{self.cliente.nome}
        """

class Historico:
    def __init__(self):
        self._transacoes = []
    @property
    def transacoes(self):
        return self._transacoes
    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            }
        )

class Transacao(abc.ABC):
    @property
    @property
    @abc.abstractmethod
    def valor(self):
        pass
    @classmethod
    @abc.abstractmethod
    def registrar(self, conta):
        pass
    
class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor
    @property
    def valor(self):
        return self._valor
    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)
                   

class Deposito(Transacao):  
    def __init__(self, valor):
        self._valor = valor
    @property
    def valor(self):
        return self._valor
    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

def menu():
    menu = f"""\
    ========== MENU ==========
    [d]\tDEPOSITAR
    [s]\tSACAR
    [e]\tEXTRATO
    [nc]\tNOVA CONTA
    [lc]\tLISTAR CONTAS
    [nu]\tNOVO USUÁRIO
    [q]\tSAIR
    ===========================
    """
    return input(textwrap.dedent(menu))

def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None

def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("====CLIENTE NÃO POSSUI CONTA====")
        return
    
    return cliente.contas[0]

def depositar(clientes):
    cpf = input("DIGITE O CPF DO CLIENTE: ")
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print("====CLIENTE NÃO ENCONTRADO====")
        return
    valor = float(input("DIGITE O VALOR DO DEPÓSITO: "))
    transacao = Deposito(valor)
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    cliente.realizar_transacao(conta, transacao)

def sacar(clientes):
    cpf = input("DIGITE O CPF DO CLIENTE: ")
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print("====CLIENTE NÃO ENCONTRADO====")
        return
    valor = float(input("DIGITE O VALOR DO SAQUE: "))
    transacao = Saque(valor)
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    cliente.realizar_transacao(conta, transacao)

def exibir_extrato(clientes):
    cpf = input("DIGITE O CPF DO CLIENTE: ")
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print("====CLIENTE NÃO ENCONTRADO====")
        return
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    print(f"\n====****EXTRATO****====")
    transacoes = conta.historico.transacoes
    extrato = ""
    if not transacoes:
        extrato = "NENHUMA TRANSAÇÃO REALIZADA!"
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['tipo']}:\n\tR${transacao['valor']:.2f}, {transacao['data']}"
    print(extrato)
    print(f"\nSALDO: R${conta.saldo:.2f}")
    print("=======================")

def criar_cliente(clientes):
    cpf = input("DIGITE O CPF DO CLIENTE: ")
    cliente = filtrar_cliente(cpf, clientes)
    if cliente:
        print("====CLIENTE JÁ CADASTRADO====")
        return
    nome = input("DIGITE O NOME DO CLIENTE: ")
    data_nascimento = input("DIGITE A DATA DE NASCIMENTO DO CLIENTE (DD/MM/AAAA): ")
    endereco = input("DIGITE O ENDEREÇO DO CLIENTE(LOGRADOURO, NRO, BAIRRO, CIDADE/SIGLA DO ESTADO): ")

    cliente = PessoaFisica(nome=nome, cpf=cpf, endereco=endereco, data_nascimento=data_nascimento)
    clientes.append(cliente)
    print(f"====CLIENTE CRIADO COM SUCESSO!====\nBEM VINDO AO BANCO DIO, {nome.upper()}!")

def criar_conta(clientes, numero_conta, contas):
    cpf = input("DIGITE O CPF DO CLIENTE: ")
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print("====CLIENTE NÃO ENCONTRADO====")
        return
    conta = ContaCorrente.nova_conta(numero=numero_conta, cliente=cliente)
    contas.append(conta)
    cliente.contas.append(conta)
    print(f"====CONTA CRIADA COM SUCESSO!====\nAGÊNCIA:\t{conta._agencia},\tCONTA:\t{conta.numero}")

def listar_contas(clientes, contas):
    for conta in contas:
        print("=" * 100)
        print(textwrap.dedent(str(conta)))
    
def main():
    clientes = []
    contas = []

    while True:
        opcao = menu()
        if opcao == "d":
            depositar(clientes)
        elif opcao == "s":
            sacar(clientes)
        elif opcao == "e":
            exibir_extrato(clientes)
        elif opcao == "nc":
            numero_conta = len(contas) + 1
            criar_conta(clientes, numero_conta, contas)
        elif opcao == "lc":
            listar_contas(clientes, contas)
        elif opcao == "nu":
            criar_cliente(clientes)
        elif opcao == "q":
            break
        else:
            print("OPÇÃO INVÁLIDA! TENTE NOVAMENTE.")

main()