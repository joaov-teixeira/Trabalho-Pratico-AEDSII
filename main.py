# Importa as funções dos outros arquivos
from Dados import gerar_lista_alunos
from Parametros import obter_parametros_armazenamento
from Serializacao import simular_escrita
from Estatisticas import calcular_e_exibir_estatisticas

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
        simular_escrita(alunos, configuracao)
        print("\nPróximo passo: Cálculo de Estatísticas.")
        dados_simulacao = simular_escrita(alunos, configuracao)
        # 4. Cálculo de estatísticas
        if dados_simulacao:
            # Pega o tamanho do registro (para modo fixo)
            tamanho_reg = dados_simulacao.get("tamanho_registro")
            
            # Chama a função de estatísticas
            calcular_e_exibir_estatisticas(
                dados_simulacao["lista_blocos"], 
                configuracao,
                tamanho_reg
            )
        else:
            print("Simulação falhou. Estatísticas não serão calculadas.")
    else:
        print("\nEncerrando o programa. Falha na Geração de Dados ou na Configuração.")
if __name__ == "__main__":
    main()