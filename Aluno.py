from faker import Faker
import random

# Inicializando o Faker (vamos usar o 'pt_BR' para dados brasileiros)
fake = Faker('pt_BR')

class Aluno:
    def __init__(self):
        # Campos de String (Nome, CPF, Curso, Filiação)
        self.nome = fake.name()
        self.cpf = fake.cpf().replace('.', '').replace('-', '') # CPF com 11 dígitos
        self.curso = random.choice(["Eng. Software", "Ciencia da Computacao", "Sistemas de Informacao", "Eng. Computacao"])
        self.filiacao_mae = fake.name('female')
        self.filiacao_pai = fake.name('male')

        # Campos de Inteiro (Matrícula, Ano de Ingresso)
        self.matricula = random.randint(100000000, 999999999) # Inteiro de 9 dígitos
        self.ano_ingresso = random.randint(2018, 2024) # Inteiro de 4 dígitos

        # Campo Float (CA)
        self.ca = round(random.uniform(0.0, 10.0), 2) # Float com 2 casas decimais

    def __str__(self):
        # Um método 'toString' para facilitar a visualização dos dados gerados
        return (f"Matrícula: {self.matricula}\n"
                f"Nome: {self.nome}\n"
                f"CPF: {self.cpf}\n"
                f"Curso: {self.curso}\n"
                f"Mãe: {self.filiacao_mae}\n"
                f"Pai: {self.filiacao_pai}\n"
                f"Ano: {self.ano_ingresso}\n"
                f"CA: {self.ca}\n"
                "--------------------")