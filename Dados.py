# Importa a classe Aluno do arquivo aluno.py
from Aluno import Aluno

def gerar_lista_alunos():
    """
    Solicita ao usuário o número total de registros a serem gerados [cite: 58]
    e cria a lista de alunos fictícios.
    """
    print("--- PASSO 1: Geração dos Dados ---")
    try:
        # Permite ao usuário definir o número total de registros
        num_registros = int(input("Digite o número total de registros a serem gerados: "))
        if num_registros <= 0:
            print("Por favor, digite um número positivo.")
            return []
            
        print(f"\nGerando {num_registros} registros de alunos...")
        # Criar um conjunto de registros de alunos com valores fictícios 
        lista_alunos = [Aluno() for _ in range(num_registros)]
        print("Registros gerados com sucesso.")
        
        return lista_alunos

    except ValueError:
        print("Entrada inválida. Por favor, digite um número inteiro.")
        return []