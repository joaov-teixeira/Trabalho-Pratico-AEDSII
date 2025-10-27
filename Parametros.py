def obter_parametros_armazenamento():
    """
    Solicita ao usuário os parâmetros da simulação:
    Tamanho do bloco, modo de armazenamento e (se aplicável) espalhamento.
    """
    print("\n--- PASSO 2: Definição dos Parâmetros de Armazenamento ---")
    
    # 1. Obter Tamanho do Bloco [cite: 60]
    try:
        tamanho_bloco = int(input("1. Digite o tamanho máximo do bloco (em bytes): "))
        if tamanho_bloco <= 0:
            print("Tamanho do bloco deve ser um número positivo.")
            return None
    except ValueError:
        print("Entrada inválida. Digite um número inteiro.")
        return None

    # 2. Obter Modo de Armazenamento [cite: 61]
    print("\n2. Escolha o modo de armazenamento:")
    print("   (1) Registros de tamanho fixo") # [cite: 26]
    print("   (2) Registros de tamanho variável") # [cite: 27]
    
    try:
        modo = int(input("   Escolha (1 ou 2): "))
        
        if modo == 1:
            modo_armazenamento = "FIXO"
            modo_espalhamento = None # Não se aplica
            
        elif modo == 2:
            modo_armazenamento = "VARIAVEL"
            
            # 3. Obter Sub-modo (se for variável) [cite: 63]
            print("\n3. Escolha o modo de registros variáveis:")
            print("   (a) Contíguos (sem espalhamento)") # [cite: 29]
            print("   (b) Espalhados (fragmentados entre blocos)") # [cite: 30]
            
            sub_modo = input("   Escolha (a ou b): ").lower()
            
            if sub_modo == 'a':
                modo_espalhamento = "CONTIGUO"
            elif sub_modo == 'b':
                modo_espalhamento = "ESPALHADO"
            else:
                print("Escolha inválida (deve ser 'a' ou 'b').")
                return None
        else:
            print("Escolha inválida (deve ser '1' ou '2').")
            return None
            
    except ValueError:
        print("Entrada inválida. Digite um número.")
        return None

    # Retorna um dicionário com as configurações
    config = {
        "tamanho_bloco": tamanho_bloco,
        "modo_armazenamento": modo_armazenamento,
        "modo_espalhamento": modo_espalhamento
    }
    
    print("\n--- Configuração Definida ---")
    print(f"Tamanho do Bloco: {config['tamanho_bloco']} bytes")
    print(f"Modo: {config['modo_armazenamento']}")
    if config['modo_espalhamento']:
        print(f"Sub-modo: {config['modo_espalhamento']}")
    print("-----------------------------")
    
    return config