import struct
import os       
import shutil
from Aluno import Aluno


PASTA_BLOCOS = "blocos_dat"

# Caractere de preenchimento (padding) usado em todo o módulo
PADDING_CHAR = b'#' 

# Define os tamanhos máximos para os campos de string
TAM_MATRICULA = 9
TAM_CPF = 14
TAM_NOME = 50
TAM_CURSO = 30
TAM_MAE = 30
TAM_PAI = 30
    
# --- NOVO: Constantes para o Modo Variável ---
# Usaremos 'H' (unsigned short) para o prefixo de tamanho. 
# Isso ocupa 2 bytes e pode armazenar tamanhos de até 65.535 bytes.
TAMANHO_PREFIXO_FORMAT = 'H'
TAMANHO_PREFIXO_BYTES = struct.calcsize(TAMANHO_PREFIXO_FORMAT)
# Delimitador interno para os campos de string
DELIMITADOR_CAMPO = b'\x00' # Byte Nulo
# Flag de Continuidade (Most Significant Bit para 2 bytes)
# 0x8000 = 1000000000000000 em binário
FLAG_CONTINUACAO = 0x8000

# --- PASSO 3.1: SERIALIZAÇÃO ---

def serializar_aluno_fixo(aluno):
    """
    Converte um objeto Aluno em uma sequência de bytes de TAMANHO FIXO.
    Todos os campos de string são preenchidos até seu tamanho máximo.
    """

    # 1. Empacotar campos numéricos (int e float)
    # 'i' = integer (4 bytes)
    # 'f' = float (4 bytes)
    bytes_numericos = struct.pack(
        'if', 
        aluno.ano_ingresso, 
        aluno.ca
    )

    # 2. Converter e preencher (pad) campos de string
    bytes_matricula = aluno.matricula.encode('utf-8').ljust(TAM_MATRICULA, PADDING_CHAR)
    bytes_cpf = aluno.cpf.encode('utf-8').ljust(TAM_CPF, PADDING_CHAR)
    bytes_nome = aluno.nome.encode('utf-8').ljust(TAM_NOME, PADDING_CHAR)
    bytes_curso = aluno.curso.encode('utf-8').ljust(TAM_CURSO, PADDING_CHAR)
    bytes_mae = aluno.filiacao_mae.encode('utf-8').ljust(TAM_MAE, PADDING_CHAR)
    bytes_pai = aluno.filiacao_pai.encode('utf-8').ljust(TAM_PAI, PADDING_CHAR)

    # 3. Concatenar todos os bytes em uma única sequência
    registro_bytes = (
        bytes_numericos +
        bytes_matricula +
        bytes_cpf +
        bytes_nome +
        bytes_curso +
        bytes_mae +
        bytes_pai
    )
    
    # Tamanho total fixo: (4+4) + 9 + 14 + 50 + 30 + 30 + 30 = 171 bytes
    return registro_bytes

#

def serializar_aluno_variavel(aluno):
    """
    Converte um objeto Aluno em uma sequência de bytes de TAMANHO VARIÁVEL.
    Campos numéricos têm tamanho fixo, strings têm tamanho real.
    """
    # 1. Empacotar campos numéricos (tamanho fixo)
    bytes_numericos = struct.pack(
        'if', 
        aluno.ano_ingresso, 
        aluno.ca
    ) # 4 + 4 = 8 bytes

    # 2. Coletar campos de string como bytes
    bytes_strings_lista = [
        aluno.matricula.encode('utf-8'),
        aluno.cpf.encode('utf-8'),
        aluno.nome.encode('utf-8'),
        aluno.curso.encode('utf-8'),
        aluno.filiacao_mae.encode('utf-8'),
        aluno.filiacao_pai.encode('utf-8')
    ]

    # 3. Juntar os campos de string usando o delimitador
    bytes_strings_juntos = DELIMITADOR_CAMPO.join(bytes_strings_lista)

    # 4. Concatenar numericos e strings para formar o "payload"
    registro_payload = bytes_numericos + bytes_strings_juntos
    
    return registro_payload

def preparar_diretorio_blocos(configuracao):
    """
    Limpa e (re)cria o diretório de blocos, se o usuário solicitou.
    """
    if configuracao["gerar_blocos_individuais"]:
        try:
            if os.path.exists(PASTA_BLOCOS):
                shutil.rmtree(PASTA_BLOCOS) # Limpa o diretório antigo
            os.makedirs(PASTA_BLOCOS)
            print(f"Diretório '{PASTA_BLOCOS}' preparado para blocos individuais.")
        except OSError as e:
            print(f"Erro ao preparar o diretório '{PASTA_BLOCOS}': {e}")
            # Desliga a flag se não conseguir criar a pasta
            configuracao["gerar_blocos_individuais"] = False

# --- NOVA FUNÇÃO AUXILIAR INTERNA ---
def _escrever_bloco(file_principal, bloco_bytes, configuracao, num_bloco):
    """
    Escreve o bloco no arquivo principal e, opcionalmente, 
    em um arquivo individual.
    """
    # 1. Escreve no arquivo principal (sempre) 
    file_principal.write(bloco_bytes)
    
    # 2. Escreve em arquivo individual (opcional)
    if configuracao["gerar_blocos_individuais"]:
        nome_bloco = f"{PASTA_BLOCOS}/bloco_{num_bloco}.dat"
        try:
            with open(nome_bloco, "wb") as f_bloco:
                f_bloco.write(bloco_bytes)
        except IOError as e:
            print(f"Erro ao escrever bloco individual '{nome_bloco}': {e}")



def _processar_modo_fixo(alunos, configuracao):
    """
    Processa e grava os alunos no modo de tamanho fixo.
    Retorna uma lista com os bytes úteis de cada bloco (para estatísticas).
    """
    tamanho_bloco = configuracao["tamanho_bloco"]
    
    # Serializa o primeiro aluno para descobrir o tamanho fixo
    if not alunos:
        print("Nenhum aluno para processar.")
        return []
        
    registro_teste_bytes = serializar_aluno_fixo(alunos[0])
    tamanho_registro = len(registro_teste_bytes)
    
    print(f"Tamanho de cada registro: {tamanho_registro} bytes")

    # Regra 4.a: "Cada registro deve ser armazenado integralmente dentro de um único bloco" 
    if tamanho_registro > tamanho_bloco:
        print(f"ERRO: O tamanho do registro ({tamanho_registro}b) é maior que o tamanho do bloco ({tamanho_bloco}b).")
        print("Não é possível continuar no modo Fixo.")
        return None # Retorna None para indicar falha

    # Calcula quantos registros cabem em um bloco
    regs_por_bloco = tamanho_bloco // tamanho_registro
    print(f"Cada bloco de {tamanho_bloco} bytes comportará {regs_por_bloco} registros.")
    
    lista_blocos_info = [] # Lista para guardar os bytes úteis de cada bloco
    bloco_atual_bytes = bytearray()
    registros_no_bloco_atual = 0
    num_bloco_atual = 1
    # Abre o arquivo .DAT para escrita binária ('wb') 
    try:
        with open("alunos.dat", "wb") as file:
            for aluno in alunos:
                # Se o bloco estiver cheio, finalize-o e grave-o
                if registros_no_bloco_atual == regs_por_bloco:
                    # 1. Calcula o espaço usado (útil)
                    bytes_usados = len(bloco_atual_bytes)
                    lista_blocos_info.append(bytes_usados)
                    
                    # 2. Preenche o restante do bloco com padding
                    padding_size = tamanho_bloco - bytes_usados
                    bloco_atual_bytes.extend(PADDING_CHAR * padding_size)
                    
                    # 3. Grava o bloco cheio no arquivo
                    #file.write(bloco_atual_bytes)
                    _escrever_bloco(file, bloco_atual_bytes, configuracao, num_bloco_atual)
                    num_bloco_atual += 1 

                    # 4. Inicia um novo bloco
                    bloco_atual_bytes = bytearray()
                    registros_no_bloco_atual = 0

                # Adiciona o registro serializado ao bloco atual
                bloco_atual_bytes.extend(serializar_aluno_fixo(aluno))
                registros_no_bloco_atual += 1

            # Após o loop, grava o último bloco (que pode não estar cheio)
            if registros_no_bloco_atual > 0:
                bytes_usados = len(bloco_atual_bytes)
                lista_blocos_info.append(bytes_usados)
                
                # Preenche e grava o último bloco
                padding_size = tamanho_bloco - bytes_usados
                bloco_atual_bytes.extend(PADDING_CHAR * padding_size)
                #file.write(bloco_atual_bytes)
                _escrever_bloco(file, bloco_atual_bytes, configuracao, num_bloco_atual)
                # num_bloco_atual += 1 # (Opcional, se quiser contar)

        print(f"\nArquivo 'alunos.dat' gerado com sucesso!")
        # Retorna a lista E o tamanho do registro
        return {"lista_blocos": lista_blocos_info, "tamanho_registro": tamanho_registro}
        
    except IOError as e:
        print(f"Erro ao escrever o arquivo 'alunos.dat': {e}")
        return None

# --- ATUALIZAÇÃO NA FUNÇÃO PRINCIPAL ---

def _processar_modo_variavel_contiguo(alunos, configuracao):
    """
    Processa e grava os alunos no modo variável SEM espalhamento.
    """
    tamanho_bloco = configuracao["tamanho_bloco"]
    lista_blocos_info = [] # Guarda os bytes úteis de cada bloco
    bloco_atual_bytes = bytearray()
    num_bloco_atual = 1 # <-- NOVO: Contador de blocos

    try:
        with open("alunos.dat", "wb") as file:
            for aluno in alunos:
                # 1. Serializar o "payload" (dados reais)
                registro_payload = serializar_aluno_variavel(aluno)
                tamanho_payload = len(registro_payload)
                
                # 2. Criar o prefixo de tamanho e calcular o tamanho total
                bytes_prefixo_tamanho = struct.pack(TAMANHO_PREFIXO_FORMAT, tamanho_payload)
                tamanho_total_registro = TAMANHO_PREFIXO_BYTES + tamanho_payload

                # 3. Verificar se o registro cabe em um bloco VAZIO
                if tamanho_total_registro > tamanho_bloco:
                    print(f"AVISO: Registro (Aluno: {aluno.nome}) tem {tamanho_total_registro} bytes, "
                          f"que é maior que o tamanho do bloco ({tamanho_bloco} bytes). Registro será pulado.")
                    continue

                # 4. Verificar espaço disponível no bloco atual
                espaco_disponivel = tamanho_bloco - len(bloco_atual_bytes)

                # 5. Aplicar a Regra "Sem Espalhamento" 
                if tamanho_total_registro > espaco_disponivel:
                    # Não cabe. Mover registro para o próximo bloco.
                    
                    # 5a. Finalizar o bloco atual
                    bytes_usados_bloco_anterior = len(bloco_atual_bytes)
                    lista_blocos_info.append(bytes_usados_bloco_anterior)
                    
                    # 5b. Preencher o restante com padding
                    padding_size = tamanho_bloco - bytes_usados_bloco_anterior
                    bloco_atual_bytes.extend(PADDING_CHAR * padding_size)
                    
                    # 5c. Gravar o bloco antigo
                    #file.write(bloco_atual_bytes)
                    _escrever_bloco(file, bloco_atual_bytes, configuracao, num_bloco_atual)
                    num_bloco_atual += 1

                    # 5d. Iniciar novo bloco JÁ COM o registro atual
                    bloco_atual_bytes = bytearray()
                    bloco_atual_bytes.extend(bytes_prefixo_tamanho + registro_payload)
                else:
                    # Cabe. Adicionar ao bloco atual.
                    bloco_atual_bytes.extend(bytes_prefixo_tamanho + registro_payload)

            # Gravar o último bloco (que pode não estar cheio)
            if len(bloco_atual_bytes) > 0:
                bytes_usados = len(bloco_atual_bytes)
                lista_blocos_info.append(bytes_usados)
                
                # Preenche e grava o último bloco
                padding_size = tamanho_bloco - bytes_usados
                bloco_atual_bytes.extend(PADDING_CHAR * padding_size)
                #file.write(bloco_atual_bytes)
                _escrever_bloco(file, bloco_atual_bytes, configuracao, num_bloco_atual)

        print(f"\nArquivo 'alunos.dat' gerado com sucesso!")
        # Retorna dados para estatísticas (sem tamanho fixo)
        return {"lista_blocos": lista_blocos_info, "tamanho_registro": None} 

    except IOError as e:
        print(f"Erro ao escrever o arquivo 'alunos.dat': {e}")
        return None
    
def _processar_modo_variavel_espalhado(alunos, configuracao):
    """
    Processa e grava os alunos no modo variável COM espalhamento (fragmentação).
    """
    tamanho_bloco = configuracao["tamanho_bloco"]
    lista_blocos_info = [] # Guarda os bytes úteis de cada bloco
    bloco_atual_bytes = bytearray()
    num_bloco_atual = 1 # <-- NOVO: Contador de blocos

    indice_aluno = 0
    registro_payload_atual = None
    bytes_escritos_do_payload = 0

    try:
        with open("alunos.dat", "wb") as file:
            
            # Loop 'while' pois um aluno pode precisar de várias iterações (blocos)
            while indice_aluno < len(alunos):
                
                # 1. Obter o payload do aluno (se for um novo)
                if registro_payload_atual is None:
                    aluno = alunos[indice_aluno]
                    registro_payload_atual = serializar_aluno_variavel(aluno)
                    bytes_escritos_do_payload = 0
                    
                    if (TAMANHO_PREFIXO_BYTES + 1) > tamanho_bloco:
                         print(f"ERRO: Tamanho do bloco ({tamanho_bloco}b) é muito pequeno. "
                               f"Não cabe nem o prefixo ({TAMANHO_PREFIXO_BYTES}b) + 1 byte de dado. Abortando.")
                         return None # Erro fatal

                # 2. Calcular o que falta escrever do registro atual
                payload_total = len(registro_payload_atual)
                payload_restante = payload_total - bytes_escritos_do_payload
                
                # 3. Calcular espaço disponível no bloco
                espaco_disponivel_no_bloco = tamanho_bloco - len(bloco_atual_bytes)

                # 4. Verificar se o bloco está "funcionalmente cheio"
                # (Não cabe nem um prefixo + 1 byte de dado)
                if espaco_disponivel_no_bloco < (TAMANHO_PREFIXO_BYTES + 1):
                    # Bloco cheio. Finalizar, gravar e começar um novo.
                    bytes_usados = len(bloco_atual_bytes)
                    lista_blocos_info.append(bytes_usados)
                    
                    padding_size = tamanho_bloco - bytes_usados
                    bloco_atual_bytes.extend(PADDING_CHAR * padding_size)
                    
                    #file.write(bloco_atual_bytes)
                    _escrever_bloco(file, bloco_atual_bytes, configuracao, num_bloco_atual)
                    num_bloco_atual += 1
                    bloco_atual_bytes = bytearray()
                    
                    # Continua o loop com O MESMO registro, mas em um novo bloco
                    continue 

                # 5. Calcular quanto payload podemos escrever neste bloco
                espaco_para_payload_neste_bloco = espaco_disponivel_no_bloco - TAMANHO_PREFIXO_BYTES

                if payload_restante <= espaco_para_payload_neste_bloco:
                    # --- 5a. O restante do registro CABE ---
                    
                    tamanho_chunk = payload_restante
                    prefixo_valor = tamanho_chunk # MSB = 0 (sem flag)
                    
                    # Obter os dados (do ponto onde paramos até o fim)
                    chunk_data = registro_payload_atual[bytes_escritos_do_payload : ]
                    
                    # Avançar para o PRÓXIMO aluno
                    indice_aluno += 1
                    registro_payload_atual = None # Limpa para carregar o próximo
                    
                else:
                    # --- 5b. O restante NÃO CABE (VAMOS ESPALHAR) ---
                    
                    tamanho_chunk = espaco_para_payload_neste_bloco
                    prefixo_valor = tamanho_chunk | FLAG_CONTINUACAO # MSB = 1 (com flag)
                    
                    # Obter os dados (apenas o pedaço que cabe)
                    inicio_chunk = bytes_escritos_do_payload
                    fim_chunk = bytes_escritos_do_payload + tamanho_chunk
                    chunk_data = registro_payload_atual[inicio_chunk : fim_chunk]
                    
                    # Atualizar o offset para O MESMO aluno
                    bytes_escritos_do_payload += tamanho_chunk
                    # Não avançamos o indice_aluno
                
                # 6. Escrever o prefixo e o chunk no bloco
                bytes_prefixo = struct.pack(TAMANHO_PREFIXO_FORMAT, prefixo_valor)
                bloco_atual_bytes.extend(bytes_prefixo + chunk_data)
                
            # --- Fim do While ---
            
            # 7. Gravar o último bloco
            if len(bloco_atual_bytes) > 0:
                bytes_usados = len(bloco_atual_bytes)
                lista_blocos_info.append(bytes_usados)
                
                padding_size = tamanho_bloco - bytes_usados
                bloco_atual_bytes.extend(PADDING_CHAR * padding_size)
                #file.write(bloco_atual_bytes)
                _escrever_bloco(file, bloco_atual_bytes, configuracao, num_bloco_atual)
        print(f"\nArquivo 'alunos.dat' gerado com sucesso!")
        return {"lista_blocos": lista_blocos_info, "tamanho_registro": None} 

    except IOError as e:
        print(f"Erro ao escrever o arquivo 'alunos.dat': {e}")
        return None
    except Exception as e:
        print(f"Erro inesperado no processamento com espalhamento: {e}")
        return None

def simular_escrita(alunos, configuracao):
    """
    Função principal do Passo 3:
    Organiza os registros em blocos e grava no arquivo .DAT
    """
    print("\n--- PASSO 3: Iniciando Simulação de Escrita ---")
    
    modo = configuracao["modo_armazenamento"]
    dados_estatisticas = None # Variável para guardar o retorno
    
    if modo == "FIXO":
        print("Modo selecionado: Tamanho Fixo")
        dados_estatisticas = _processar_modo_fixo(alunos, configuracao)
        
    elif modo == "VARIAVEL":
        print("Modo selecionado: Tamanho Variável (Não implementado)")
        sub_modo = configuracao["modo_espalhamento"]
        print(f"Modo selecionado: Tamanho Variável")
        
        if sub_modo == "CONTIGUO":
            print("Sub-modo: Contíguo (sem espalhamento)")
            dados_estatisticas = _processar_modo_variavel_contiguo(alunos, configuracao)
        
        elif sub_modo == "ESPALHADO":
            print("Sub-modo: Espalhado (fragmentado)")
            dados_estatisticas = _processar_modo_variavel_espalhado(alunos, configuracao)
            pass
        pass

    return dados_estatisticas # Retorna os dados para o main.py