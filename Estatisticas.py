def calcular_e_exibir_estatisticas(lista_blocos_info, configuracao, tamanho_registro_fixo=None):
    """
    Calcula e exibe as estatísticas de armazenamento
    'lista_blocos_info' contém os bytes úteis de cada bloco
    'tamanho_registro_fixo' é usado para o modo fixo
    """
    print("\n--- PASSO 4 e 5: Estatísticas de Armazenamento ---")

    if not lista_blocos_info:
        print("Nenhum dado de bloco foi gerado. Não é possível calcular estatísticas.")
        return

    tamanho_bloco = configuracao["tamanho_bloco"]
    modo = configuracao["modo_armazenamento"]

    # --- 1. Número total de blocos utilizados ---
    total_blocos = len(lista_blocos_info) 
    
    # --- Cálculo de Bytes ---
    total_bytes_uteis = sum(lista_blocos_info)
    total_bytes_alocados = total_blocos * tamanho_bloco

    # --- 4. Eficiência de armazenamento ---
    # (% de bytes ocupados por dados úteis
    eficiencia_total = (total_bytes_uteis / total_bytes_alocados) * 100

    # --- 3. Número de blocos parcialmente utilizados ---
    blocos_parciais = 0
    if modo == "FIXO" and tamanho_registro_fixo:
        # No modo fixo, um bloco "parcial" é o último, se ele não
        # comportou o número máximo de registros.
        regs_por_bloco = tamanho_bloco // tamanho_registro_fixo
        bytes_max_uteis_por_bloco = regs_por_bloco * tamanho_registro_fixo
        
        for bytes_usados in lista_blocos_info:
            if bytes_usados < bytes_max_uteis_por_bloco:
                blocos_parciais += 1
    else:
        # Em modo variável, qualquer bloco não 100% cheio é parcial
        for bytes_usados in lista_blocos_info:
            if bytes_usados < tamanho_bloco:
                blocos_parciais += 1 #

    # --- 5. Mapa de ocupação dos blocos (Exemplo textual) ---
    print("\n--- Mapa de Ocupação ---") #
    lista_percentuais = []
    for i, bytes_usados in enumerate(lista_blocos_info):
        percentual_ocupacao = (bytes_usados / tamanho_bloco) * 100
        lista_percentuais.append(percentual_ocupacao)
        print(f"Bloco {i+1}: {bytes_usados} bytes utilizados ({percentual_ocupacao:.2f}% cheio)")

    # --- 2. Percentual médio de ocupação ---
    # (É o mesmo que a eficiência total)
    percentual_medio = sum(lista_percentuais) / total_blocos

    # --- Exibição do Resumo Estatístico ---
    print("\n--- Resumo Estatístico ---")
    print(f"1. Número total de blocos utilizados: {total_blocos}")
    print(f"2. Percentual médio de ocupação: {percentual_medio:.2f}%")
    print(f"3. Número de blocos parcialmente utilizados: {blocos_parciais}")
    print(f"4. Eficiência de armazenamento (bytes úteis): {eficiencia_total:.2f}%")
    print("--------------------------------------------------")