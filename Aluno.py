from faker import Faker
import random

# Inicializando o Faker (usando o 'pt_BR' para dados brasileiros)
fake = Faker('pt_BR')

class Aluno:
    def __init__(self):
        # campo de INT:
        self.ano_ingresso = random.randint(2018, 2025) # Inteiro de 4 dígitos
        
        '''
        Formatando a matricula como padroes da UFOP
        XX.Y.ABCD
        onde XX são os dois ultimos numeros do ano de ingresso no curso;
        Y é o semestre(1 ou 2);
        e ABCD são numeros sequenciais da matricula, que para o nosso serão aleatorios.
        '''
        
        xx = str(self.ano_ingresso)[-2:]  # Pega os últimos 2 dígitos (ex: 2024 -> "24")
        y = random.choice([1, 2])         # Período (1 ou 2)
        abcd = random.randint(1000, 9999) # Parte aleatória de 4 dígitos
        
        # 3. Montamos a Matrícula formatada como STRING
        self.matricula = f"{xx}.{y}.{abcd}"
        
        # Campos de String (Nome, CPF, Curso, Filiação)
        self.nome = fake.name()
        self.cpf = fake.cpf()#.replace('.', '').replace('-', '') # CPF com 11 dígitos
        self.curso = random.choice(["Engenharia de Produção", "Engenharia Elétrica", "Sistemas de Informação", "Engenharia da Computação"])
        self.filiacao_mae = fake.name_female()
        self.filiacao_pai = fake.name_male()

        # Campos de Inteiro (Matrícula, Ano de Ingresso)
        #self.matricula = random.randint(100000000, 999999999) # Inteiro de 9 dígitos
        

        # Campo Float (CA)
        self.ca = round(random.uniform(0.0, 10.0), 2) # Float com 2 casas decimais

    def __str__(self):
        # Um método 'toString' para facilitar a visualização dos dados gerados
        return (
                f"Nome: {self.nome}\n"
                f"Curso: {self.curso}\n"
                f"Matrícula: {self.matricula}\n"
                f"Ano: {self.ano_ingresso}\n"
                f"CA: {self.ca}\n"
                f"CPF: {self.cpf}\n"
                f"Mãe: {self.filiacao_mae}\n"
                f"Pai: {self.filiacao_pai}\n"
                "--------------------")