#Importação do time para dar pausas entre execuções
import time

#Variável global para armazenar o usuário atual logado, definido como none (nenhum usuário)
usuario_logado = None

#Função que imprime o menu principal
def menu():
    impressao_menu = '''
============== LINK CAR ==============
[1] - Criar conta
[2] - Login
[3] - Visualizar/Gerenciar contas
[4] - Registrar carro
[5] - Visualizar/Gerenciar carros
[6] - Registrar problema no carro
[7] - Integrantes
[8] - Sair
=======================================
'''
    print(impressao_menu)

#Função para ler e validar se a opção escolhida é válida
def ler_opcao(mensagem):
    while True:
        try:
            opcao = int(input(mensagem))
            return opcao
        except ValueError:
            print('Por favor, apenas utilize números!')
            input('Pressione Enter para tentar novamente...')

#Função para criar uma conta nova
def criar_conta(numero_conta, contas):
    email = input('Digite o email: ')
    conta = filtrar_contas(email, contas)
    
    if conta:
        print('Já existe um usuário com este email cadastrado!')
        return
    senha = input('Digite a senha: ')
    nome = input('Digite o nome completo: ')
    endereco = input('Digite o endereço (Rua - Número - Bairro - Cidade - Estado): ')
    contas.append({'nome': nome, 'senha': senha, 'endereco': endereco, 'email': email, 'numero_conta': numero_conta})
    print('Conta criada com sucesso!')
    
    input('Pressione Enter para voltar ao menu principal...')

#Função para listar contas (exceto senha)
def listar_contas(contas):
    for conta in contas:
        print('======================================================')
        print(f'Conta N°: {conta["numero_conta"]}')
        print(f"Nome: {conta['nome']}")
        print(f"Email: {conta['email']}")
        print(f"Endereço: {conta['endereco']}")
        if 'veiculos' in conta:
            print("Veículos registrados:")
            for veiculo in conta['veiculos']:
                print(f"- {veiculo['marca']} {veiculo['modelo']}, placa: {veiculo['placa']}")
        print('======================================================')
    time.sleep(5)

#Função que verifica se uma conta com o email fornecido já existe
def filtrar_contas(email, contas):
    contas_filtradas = [conta for conta in contas if conta['email'] == email]
    return contas_filtradas[0] if contas_filtradas else None

#Função de login
def login(contas):
    global usuario_logado  # Para mexer na variável global
    if usuario_logado:
        print('======================= LOGIN =======================')
        print(f'Você está logado como {usuario_logado["nome"]}')
        print('[1] - Entrar em outra conta')
        print('[2] - Sair da conta atual')
        print('[3] - Voltar ao menu principal')
        print('=====================================================')
        opcao = ler_opcao('Escolha uma opção: ')
        
        if opcao == 1:
            usuario_logado = None
            login(contas) 
        elif opcao == 2:
            usuario_logado = None
            print('Você saiu da conta.')
        elif opcao == 3:
            return
    else:
        email_inserido = input('Digite o email: ')
        conta = filtrar_contas(email_inserido, contas)
        
        if conta:
            senha_inserida = input('Digite a senha: ')
            if senha_inserida == conta['senha']:
                usuario_logado = conta
                print(f'Login realizado com sucesso! Bem-vindo, {usuario_logado["nome"]}.')
            else:
                print('Senha incorreta!')
        else:
            print('Email não encontrado!')
        input('Pressione Enter para voltar ao menu principal...')

#Função para apagar contas
def apagar_conta(contas):
    if not contas:
        print('Não há contas cadastradas.')
        input('Pressione Enter para voltar ao menu principal...')
        return

    print('Contas cadastradas: ')
    listar_contas(contas)
    
    numero_conta = ler_opcao('Digite o número da conta a ser deletada: ')

    conta_encontrada = None
    for conta in contas:
        if conta['numero_conta'] == numero_conta:
            conta_encontrada = conta
            break

    if conta_encontrada:
        contas.remove(conta_encontrada)
        print(f'Conta N° {numero_conta} removida com sucesso!')
    else:
        print(f'Conta N° {numero_conta} não encontrada!')

    input('Pressione Enter para voltar ao menu principal...')

#Função para alterar informações das contas
def alterar_informacoes(contas, usuario_logado):
    print('[1] - Nome')
    print('[2] - Endereço')
    print('[3] - Email')
    print('[4] - Sair')
    opcao = ler_opcao('Escolha qual informação será alterada: ')
    match opcao:
        case 1:
            del(usuario_logado['nome'])
            novo_nome = input('Digite o novo nome: ')
            usuario_logado['nome'] = novo_nome
            print(f'Nome alterado com sucesso para {novo_nome}')
            input('Pressione Enter para retornar...')

#Submenu do gerenciamento de contas
def sub_informacoes_conta(contas):
    print('===================================== ALTERAR INFORMAÇÕES DA CONTA =====================================')
    print(f'Você está logado como {usuario_logado["nome"]}')
    print('Por questões de segurança, para alterar as informações de uma conta, você precisa estar logado nela.')
    print('[1] - Mudar de conta (Ir para a tela de login)')
    print('[2] - Alterar informações da conta')
    print('[3] - Voltar ao menu principal')
    print('========================================================================================================')
    opcao = ler_opcao('Escolha uma opção: ')
    match opcao:
        case 1:
            login(contas)
        case 2:
            alterar_informacoes(contas, usuario_logado)
        case 3:
            return
        case _:
            print('Opção inválida!')
            input('Pressione Enter para retornar ao menu principal...')

#Menu de gerenciamento de contas
def gerenciar_contas(contas):
    print('======== GERENCIAMENTO DE CONTAS ========')
    print('[1] - Visualizar contas')
    print('[2] - Apagar uma conta')
    print('[3] - Alterar informações de uma conta')
    print('[4] - Voltar ao menu principal')
    print('==========================================')
    opcao = ler_opcao('Escolha uma opção: ')
    match opcao:
        case 1:
            listar_contas(contas)
        case 2:
            apagar_conta(contas)
        case 3:
            sub_informacoes_conta(contas)
        case 4:
            return
        case _:
            print('Opção inválida!')
            input('Pressione Enter para retornar ao menu principal...')

#Função para registrar um veículo e associá-lo ao usuário logado
def registrar_veiculo(veiculos):
    global usuario_logado  #Para mexer na variável global
    print('======================== REGISTRO DE CARRO ========================')
    print(f'Você está logado como {usuario_logado["nome"]}. O carro registrado estará ligado a este usuário.')
    
    chassi = input('Por favor, informe o número do chassi do carro: ')
    
    if len(chassi) == 17:
        marca = input('Por favor, informe a marca do carro: ')
        modelo = input('Por favor, informe o modelo do carro: ')
        cor = input('Por favor, informe a cor do carro: ')
        placa = input('Por favor, informe a placa do carro (ABC1D23) ou (ABC-1234): ')
        
        veiculo = {'chassi': chassi, 'marca': marca, 'modelo': modelo, 'cor': cor, 'placa': placa}
        
        if 'veiculos' not in usuario_logado:
            usuario_logado['veiculos'] = []  
        usuario_logado['veiculos'].append(veiculo)  
        
        veiculos.append(veiculo)
        
        print(f"Veículo {marca} {modelo} registrado com sucesso para {usuario_logado['nome']}!")
    else:
        print('Número do chassi inválido!')
    
    input('Pressione Enter para retornar ao menu principal...')

#Função para visualizar os veículos cadastrados
def visualizar_veiculos():
    if 'veiculos' in usuario_logado and usuario_logado['veiculos']:
        print(f'Veículos cadastrados por {usuario_logado["nome"]}:')
        for veiculo in usuario_logado['veiculos']:
            print('=============================================')
            print(f"Marca: {veiculo['marca']}")
            print(f"Modelo: {veiculo['modelo']}")
            print(f"Cor: {veiculo['cor']}")
            print(f"Placa: {veiculo['placa']}")
            print(f"Chassi: {veiculo['chassi']}")
            print('=============================================')
    else:
        print('Você não tem veículos cadastrados.')

    input('Pressione Enter para voltar ao menu...')

#Função para apagar um veículo
def apagar_veiculo():
    if 'veiculos' not in usuario_logado or not usuario_logado['veiculos']:
        print('Você não tem veículos cadastrados.')
        input('Pressione Enter para voltar ao menu...')
        return
    
    visualizar_veiculos()
    placa = input('Informe a placa do veículo que deseja remover: ')
    
    veiculo_encontrado = None
    for veiculo in usuario_logado['veiculos']:
        if veiculo['placa'] == placa:
            veiculo_encontrado = veiculo
            break
    
    if veiculo_encontrado:
        usuario_logado['veiculos'].remove(veiculo_encontrado)
        print(f'Veículo {veiculo_encontrado["marca"]} {veiculo_encontrado["modelo"]} removido com sucesso!')
    else:
        print('Veículo não encontrado.')
    
    input('Pressione Enter para voltar ao menu...')

#Função para alterar as informações de um veículo
def alterar_informacoes_veiculo():
    if 'veiculos' not in usuario_logado or not usuario_logado['veiculos']:
        print('Você não tem veículos cadastrados.')
        input('Pressione Enter para voltar ao menu...')
        return
    
    visualizar_veiculos()
    placa = input('Informe a placa do veículo que deseja alterar: ')
    
    veiculo_encontrado = None
    for veiculo in usuario_logado['veiculos']:
        if veiculo['placa'] == placa:
            veiculo_encontrado = veiculo
            break
    
    if veiculo_encontrado:
        print(f'Alterando informações do veículo {veiculo_encontrado["marca"]} {veiculo_encontrado["modelo"]}:')
        veiculo_encontrado['marca'] = input('Informe a nova marca: ')
        veiculo_encontrado['modelo'] = input('Informe o novo modelo: ')
        veiculo_encontrado['cor'] = input('Informe a nova cor: ')
        veiculo_encontrado['placa'] = input('Informe a nova placa: ')
        print('Informações alteradas com sucesso!')
    else:
        print('Veículo não encontrado.')
    
    input('Pressione Enter para voltar ao menu...')

#Submenu de gerenciamento de veículos
def gerenciar_veiculos():
    print('======== GERENCIAMENTO DE VEÍCULOS ========')
    print('[1] - Visualizar veículos')
    print('[2] - Apagar um veículo')
    print('[3] - Alterar informações de um veículo')
    print('[4] - Voltar ao menu principal')
    print('===========================================')
    opcao = ler_opcao('Escolha uma opção: ')
    match opcao:
        case 1:
            visualizar_veiculos()
        case 2:
            apagar_veiculo()
        case 3:
            alterar_informacoes_veiculo()
        case 4:
            return
        case _:
            print('Opção inválida!')
            input('Pressione Enter para retornar ao menu...')

#Função para registrar um problema, em um veículo do usuário logado
def registrar_problema():
    if 'veiculos' not in usuario_logado or not usuario_logado['veiculos']:
        print('Você não tem veículos cadastrados.')
        input('Pressione Enter para voltar ao menu...')

    print(f"Veículos cadastrados por {usuario_logado['nome']}:")
    i = 1
    for veiculo in usuario_logado['veiculos']:
        print(f"[{i}] {veiculo['marca']} {veiculo['modelo']}, placa: {veiculo['placa']}")
        i += 1

    opcao = ler_opcao('Escolha o número do veículo para registrar o problema: ')

    if 1 <= opcao <= len(usuario_logado['veiculos']):
        veiculo_escolhido = usuario_logado['veiculos'][opcao - 1]
        problema = input('Por favor, informe o problema encontrado no veículo: ')

        if 'problemas' not in veiculo_escolhido:
            veiculo_escolhido['problemas'] = []
        
        veiculo_escolhido['problemas'].append(problema)

        print(f"Problema de '{problema}' no carro {veiculo_escolhido['marca']} {veiculo_escolhido['modelo']} "
              f"de {usuario_logado['nome']} registrado, e será verificado para um diagnóstico.")
    else:
        print('Opção inválida!')

    input('Pressione Enter para voltar ao menu...')


#Lógica principal do programa
def main():
    contas = []
    veiculos = []

    while True:
        menu()
        opcao = ler_opcao('Escolha uma opção: ')
        match opcao:
            case 1:
                numero_conta = len(contas) + 1
                criar_conta(numero_conta, contas)
            case 2:
                login(contas)
            case 3:
                if usuario_logado:
                    gerenciar_contas(contas)
                else:
                    print('Você não está logado!')
                    input('Pressione Enter para retornar...')
            case 4:
                if usuario_logado:
                    registrar_veiculo(veiculos)
                else:
                    print('Você não está logado!')
                    input('Pressione Enter para retornar...')
            case 5:
                if usuario_logado:
                    gerenciar_veiculos()
                else:
                    print('Você não está logado!')
                    input('Pressione Enter para retornar...')
            case 6:
                if usuario_logado:
                    registrar_problema()
                else:
                    print('Você não está logado!')
                    input('Pressione Enter para retornar...')
            case 7:
                print('================================== INTEGRANTES ==================================')
                print('Renato de Freitas David Campiteli - RM555627 - https://github.com/renatofdavidc')
                print('Pedro Lucas de Oliveira Bezerra - RM558439 - https://github.com/PedrinDev1447')
                print('Gabriel Santos Jablonski - RM555425 - https://github.com/Jablonski17')
                print('=================================================================================')
                input('Pressione Enter para voltar ao menu principal...')
            case 8:
                print('Saindo...')
                break
            case _:
                print('Opção inválida!')

#Executa o programa
main()
