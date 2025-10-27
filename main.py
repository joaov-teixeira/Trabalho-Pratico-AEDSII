# Importa as funções dos outros arquivos
from Dados import gerar_lista_alunos
from Parametros import obter_parametros_armazenamento

# --- Execução Principal ---
def main():
    # 1. Geração dos dados
    alunos = gerar_lista_alunos()
    
    configuracao = None
    if alunos:
        # Exibe os 3 primeiros alunos gerados apenas para conferência
        print("\n--- Amostra dos dados gerados ---")
        for aluno in alunos[:3]:
            print(aluno)
        
        # 2. Definição dos parâmetros
        configuracao = obter_parametros_armazenamento()
    
    if alunos and configuracao:
        print("\nPróximo passo: Simulação de Escrita.")
        # O Passo 3: Simulação de escrita viria aqui.
        # Nós chamaremos uma nova função, por exemplo:
        # simular_escrita(alunos, configuracao)
    else:
        print("\nEncerrando o programa. Falha na Geração de Dados ou na Configuração.")

# Garante que a função main() seja executada apenas quando este arquivo for rodado
if __name__ == "__main__":
    main()