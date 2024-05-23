from abc import ABC, abstractclassmethod, abstractproperty
from datetime import datetime
import os # Adicionado para utilizar a opção de limpar menu
import platform
import textwrap

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []
        self.indice_conta = 0

    def realizar_transacao(self, conta, transacao):
        if len(conta.historico.transacoes_do_dia()) >= 10:
            print("Limite diario excedido!")
            return

        transacao.registrar(conta)

    def adicionar_conta(self, conta):
         self.conta.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
         super().__init__(endereco)
         self.nome = nome
         self.data_nascimento = data_nascimento
         self.cpf = cpf

class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
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
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print("Saldo insuficiente para saque.")
        
        elif valor > 0:
            self._saldo -= valor
            print("Saque realizado com sucesso!")
            return True
        
        else:
            print("Falha na operacao!")
        
        return False    

    def depositar(self, valor):

        if ( valor > 0 ):
            self._saldo += valor
            print("Deposito realizado!")    
        else:
            print("Valor invalido, tente novamente!")
            return False

        return True

class ContaCorrente(Conta):

    def __init__(self, numero, cliente, limite = 500, limite_saques = 3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__]
        )

        excedeu_limite = valor > self.limite
        excedeu_saques = numero_saques >= self.limite_saques

        if excedeu_limite:
            print("Excedeu limite de saque!")

        elif excedeu_saques:
            print("Numero maximo de saques realziados!")

        else:
            return super().sacar(valor)    

        return False

    def __str__(self):
        return f"""\
            Agencia:\t{self.agencia}
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
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            }
        )
    def gerar_relatorio(self, tipo_transacao = None):
        for transacao in self._transacoes:
            if ( tipo_transacao is None or transacao["tipo"].lower() == tipo_transacao.lower()):
                yield transacao

    def transacoes_do_dia(self):
        data_atual = datetime.now().date()
        transacoes = []
        for transacao in self._transacoes:
            data_transacao = datetime.strptime(transacao["data"], "%d-%m-%Y %H:%M:%S").date()
            if data_atual == data_transacao:
                transacoes.append(transacao)
        return transacoes


class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass
    
    @abstractclassmethod
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

class ContaIterador:
    def __init__(self, contas):
        pass
    def __iter__(self):
        pass
    def __next__(self):
        pass

def log_transacao(func):
    def envelope(*args, **kwargs):
        resultado = func(*args, **kwargs)
        print(f"{datetime.now()}: {func.__name__.upper()}")
        return resultado

    return envelope

def menu():

            menu = """ 
                        BANCO PYX 3.0
            [1] Depositar
            [2] Sacar
            [3] Extrato
            [4] Cadastrar Cliente
            [5] Cadastrar Conta
            [6] Listar Contas
            [0] Sair

            =>"""
            return int(input(menu))

def criar_cliente(clientes):
    
    cpf = input("informe o CPF do cliente:")
    cliente = filtrar_cliente(cpf,clientes) 

    if cliente:
        print("Cliente ja cadastrado!")
        return

    nome = input("Digite o nome: ")
    data_nascimento = input("Digite a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Infome o endereco (logradouro, numero, bairro - cidade/sigla do estado): ")
    
    cliente = PessoaFisica(nome=nome,data_nascimento=data_nascimento,cpf=cpf, endereco=endereco)

    clientes.append(cliente)
    limpar()
    print("Cliente cadastrado!")

def filtrar_cliente(cpf, clientes):
   clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf ]
   return clientes_filtrados[0] if clientes_filtrados else None  

@log_transacao
def criar_conta(numero_conta, clientes, contas):

    cpf = input("Digite o cpf do usuario: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
         print("Cliente nao cadastrado!")
         return
    
    conta = ContaCorrente.nova_conta(cliente=cliente,
    numero=numero_conta)                                 
    contas.append(conta)
    cliente.contas.append(conta)                               
    limpar()
    print("Conta criada com sucesso!")

@log_transacao    
def listar_contas (contas):
    limpar() 
    for conta in contas:
        print("=" * 60)
        print(textwrap.dedent(str(conta)))

def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("Cliente sem conta!")
        return
    
    return cliente.contas[0]

@log_transacao
def depositar(clientes):

    cpf = input("informe o CPF do cliente:")
    cliente = filtrar_cliente(cpf,clientes)

    if not cliente:
        print("Cliente nao cadastrado!")
        return
    
    valor = float(input("Informe o valor do deposito:"))
    transacao = Deposito(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    limpar() 
    cliente.realizar_transacao(conta, transacao)   

@log_transacao
def sacar(clientes):
    
    cpf = input("informe o CPF do cliente:")
    cliente = filtrar_cliente(cpf,clientes)

    if not cliente:
        print("Cliente nao cadastrado!")
        return
    
    valor = float(input("Informe o valor do saque:"))
    transacao = Saque(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    limpar()
    cliente.realizar_transacao(conta, transacao)

@log_transacao
def exibir_extrato(clientes):

    limpar()
    cpf = input("informe o CPF do cliente:")
    cliente = filtrar_cliente(cpf,clientes) 

    if not cliente:
        print("Cliente nao cadastrado!")
        return
    
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    print("\n==================== EXTRATO ====================")
    transacoes = conta.historico.transacoes

    extrato = ""
    tem_transacao = False
    for transacao in conta.historico.gerar_relatorio():
        tem_transacao = True
        extrato += f"\n{transacao['data']}\n{transacao['tipo']}: \n\tR$ {transacao['valor']:.2f}"

    if not transacoes:
        extrato = "Nao foram encontrados registros"
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['tipo']}:\n\t R$ {transacao['valor']:.2f}"

    print(extrato)
    print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")
    print("===================================================")

def limpar():

    # Verificar o sistema operacional
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')

def main():

    clientes = []
    contas = []

    while True:
    
        opcao = menu()

        if opcao == 1: # Opcao de deposito

            depositar(clientes)

        elif opcao == 2: # Opcao de saque

            sacar(clientes)

        elif opcao == 3: # Opção de extrato

            exibir_extrato(clientes)

        elif opcao == 4: # Opção de cadastrar usuario
             
           criar_cliente(clientes) 
        
        elif opcao == 5: # Opção de cadastrar conta

           numero_conta = len(contas)+1
           criar_conta(numero_conta, clientes, contas)  
        
        elif opcao == 6: # Opção de listar conta
             
            listar_contas(contas)

        elif opcao == 0: # Opção de sair da aplicação
            print('''
            Obrigado por utilizar nosso servico!
            ''')
            break
        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")

main()