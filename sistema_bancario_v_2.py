# Programa para fazer depósitos, saques e imprimir extratos:
def main():

    # Constantes:
    NUMERO_MAXIMO_DE_SAQUES = 3
    VALOR_LIMITE_POR_SAQUE = 500

    # Inicializar dicionários:
    clientes = {}
    contas = {}
    cliente_contas = {}


    while True:
        opcao = leitura()

        if opcao.lower() == "d":
            # Solicita o CPF da conta:
            CPF = input("Informe o CPF do cliente: ")

            # Recupera as informações da conta do cliente; caso não exista o CPF, retorna conta_ok = False:
            conta_ok, saldo, extrato, numero_de_saques = recupera_informacoes_conta(CPF, contas, cliente_contas)

            # Realiza o depósito:
            if conta_ok:
                saldo, extrato = depositar(saldo, extrato)
                # Atualiza as informações da conta corrente do cliente:
                atualiza_informacoes_conta(CPF, saldo, extrato, numero_de_saques, contas, cliente_contas)
            else:
                print("\n@@@ Erro: CPF não existe. Depósito não realizado. @@@")
            

        elif opcao.lower() == "s":

            # Solicita o CPF da conta:
            CPF = input("Informe o CPF do cliente: ")

            # Recupera as informações da conta do cliente; caso não exista o CPF, retorna conta_ok = False:
            conta_ok, saldo, extrato, numero_de_saques = recupera_informacoes_conta(CPF, contas, cliente_contas)

            # Realiza o saque:
            if conta_ok:
                saldo, extrato, numero_de_saques = sacar(saldo = saldo, extrato = extrato, numero_de_saques = numero_de_saques, NUMERO_MAXIMO_DE_SAQUES = NUMERO_MAXIMO_DE_SAQUES, VALOR_LIMITE_POR_SAQUE = VALOR_LIMITE_POR_SAQUE)
                # Atualiza as informações da conta corrente do cliente:
                atualiza_informacoes_conta(CPF, saldo, extrato, numero_de_saques, contas, cliente_contas)
            else:
                print("\n@@@ Erro: CPF não existe. Saque não realizado. @@@")

        elif opcao.lower() == "e":

            # Solicita o CPF da conta:
            CPF = input("Informe o CPF do cliente: ")

            # Recupera as informações da conta do cliente; caso não exista o CPF, retorna conta_ok = False:
            conta_ok, saldo, extrato, numero_de_saques = recupera_informacoes_conta(CPF, contas, cliente_contas)

            # Imprimi o extrato:
            if conta_ok:
                exibir_extrato(saldo, extrato = extrato)
            else:
                print("\n@@@ Erro: CPF não existe. Saque não realizado. @@@")
            
        elif opcao.lower() == "nc":
            criar_conta(clientes, contas, cliente_contas)

        elif opcao.lower() == "nu":
            criar_usuario(clientes)

        elif opcao.lower() == "q":
            break
        
        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")

# Define o Menu principal e retorna o valor da opção escolhida:
def leitura():
    menu = """

    [d]  Depositar
    [s]  Sacar
    [e]  Extrato
    [nc] Nova conta
    [nu] Novo usuário
    [q]  Sair

=> """
    opcao = input(menu)
    return opcao

# função que realiza do depósito:
def depositar(saldo, extrato, /):

    # Realiza a leitura do valor a ser depositado:
    valor_a_depositar = input("Por favor, informe o valor a ser depositado: ")

    # Analisa se o valor é um número não negativo. Se negativo, retorna -1:
    valor_a_depositar = eh_numero_não_negativo(valor_a_depositar)

    # Se o valor_a_depositar é válido, realiza o depósito:
    if valor_a_depositar != -1:
        saldo += valor_a_depositar
        extrato += f"Depósito: R$ {valor_a_depositar:.2f}\n"
        print("\n=== Depósito realizado com sucesso. ===")

    # Se o valor_a_depositar não é válido, informa o erro:
    else:
        print("\n@@@ Erro: o valor informado não é válido. @@@")

    # Retorna o saldo e extrato:
    return saldo, extrato

# Função que realiza o saque:
def sacar(*, saldo, extrato, numero_de_saques, NUMERO_MAXIMO_DE_SAQUES, VALOR_LIMITE_POR_SAQUE):

    # Realiza a leitura do valor a ser sacado:
    valor_a_sacar = input("Por favor, informe o valor a ser sacado: ")

    # Analisa se o valor é um número não negativo. Se negativo, retorna -1:
    valor_a_sacar = eh_numero_não_negativo(valor_a_sacar)

    # Se o valor_a_sacar não é válido, informa o erro:
    if valor_a_sacar == -1:
        print("\n@@@ Erro: o valor informado não é válido. @@@")
        
    # Se o valor_a_sacar é superior ao saldo, informa o erro:
    elif valor_a_sacar > saldo:
        print("\n@@@ Erro: saldo insuficiente. @@@")
        
    # Se o valor_a_sacar é superior ao valor limite por saque, informa o erro:
    elif valor_a_sacar > VALOR_LIMITE_POR_SAQUE:
        print(f"\n@@@ Erro: valor superior ao limite por saque: R$ {VALOR_LIMITE_POR_SAQUE:.2f}. @@@")

    # Se o numero_de_saques é superior ao numero máximo de saques, informa o erro:
    elif numero_de_saques >= NUMERO_MAXIMO_DE_SAQUES:
        print(f"\n@@@ Erro: número de saques superior ao limite diário: {NUMERO_MAXIMO_DE_SAQUES} saques. @@@")

    # Todas condições satisfeitas, realiza-se o saque:
    else:
        saldo -= valor_a_sacar
        extrato += f"Saque:    R$ {valor_a_sacar:.2f}\n"
        numero_de_saques += 1
        print("\n=== Saque realizado com sucesso. ===")

    # Retorna o saldo e extrato atualizado:
    return saldo, extrato, numero_de_saques

# Função que realiza a impressão do extrato:
def exibir_extrato(saldo, /, *, extrato):
    print("\n================ EXTRATO ================")
    print("=== Não foram realizadas movimentações. ===" if extrato == "\n" else extrato)
    print(f"\nSaldo:    R$ {saldo:.2f}")
    print("==========================================")

# Função que cria novo usuário:
def criar_usuario(clientes):
    # Solicita o CPF do cliente:
    CPF = input("Informe o CPF (somente números): ")

    # Verifica se tem somente números:
    if CPF.isdigit() == False:
        print("\n@@@ Erro: CPF não tem somente números: novo usuário não foi criado. @@@")
        return -1
    
    # Verifica se CPF já se encontra no dicionário clientes:
    if CPF in clientes:
        print("\n@@@ Erro: CPF já se encontra no cadastro de clientes: novo usuário não foi criado. @@@")
        return -1
    
    # Solicita o nome:
    nome = input("Informe o nome completo: ")

    # Solicita a data de nascimento (dd-mm-aaaa):
    data = input("Informe a data de nascimento (dd-mm-aaaa): ")

    # Solicita o endereço:
    endereco = input("Informe o endereço (logradouro, número - bairro - cidade / sigla estado): ")

    # Atualiza o dicionário de clientes:
    clientes[CPF] = {"nome": nome, "data": data, "endereco": endereco}

    #Informa que se conseguiu criar o novo usuário:
    print("\n=== Novo usuário criado com sucesso. ===")

    # Retorna código de sucesso na operação:
    return 0

# Função que cria nova conta corrente:
def criar_conta(clientes, contas, cliente_contas):

    # Solicita o CPF da conta:
    CPF = input("Informe o CPF da conta corrente: ")

    # Verifica se o CPF já está cadastrado:
    if CPF not in clientes:
        print("\n@@@ Erro: CPF não se encontra no cadastro de clientes: nova conta corrente não foi criada. @@@")
        return -1

    # Define o número da conta corrente:
    numero_conta = len(contas) + 1

    # Cria a nova conta corrente:
    contas[("0001", numero_conta)] = {"CPF":CPF, "saldo": 0, "extrato": "\n", "numero_de_saques": 0}

    #Acrescenta a conta corrente na lista de contas do cliente:
    cliente_contas.setdefault(CPF, []).append(("0001", numero_conta))

    #Informa que se conseguiu criar a conta corrente:
    print("\n=== Conta corrente criada com sucesso. ===")

    # Retorna código de sucesso na operação:
    return 0

def recupera_informacoes_conta(CPF, contas, cliente_contas):
    # Verifica se o CPF existe:
    if CPF not in cliente_contas:
        return False, None, None, None
    
    # Recupera informações da conta cliente:
    saldo = contas[cliente_contas[CPF][0]]["saldo"]
    extrato = contas[cliente_contas[CPF][0]]["extrato"]
    numero_de_saques = contas[cliente_contas[CPF][0]]["numero_de_saques"]

    return True, saldo, extrato, numero_de_saques

def atualiza_informacoes_conta(CPF, saldo, extrato, numero_de_saques, contas, cliente_contas):
    
    # Atualiza informações da conta cliente:
    contas[cliente_contas[CPF][0]]["saldo"] = saldo
    contas[cliente_contas[CPF][0]]["extrato"] = extrato
    contas[cliente_contas[CPF][0]]["numero_de_saques"] = numero_de_saques

    return 0


# Função que verifica se a string é um número positivo, caso negativo, retorna -1:
def eh_numero_não_negativo(s):

    try:
        numero = float(s)
        if numero >= 0:

            return numero
        
    except ValueError:
        return -1
    
    return -1

main()