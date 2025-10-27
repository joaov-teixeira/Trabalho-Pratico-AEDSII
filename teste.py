from faker import Faker

# Inicializa o Faker
fake = Faker('pt_BR')

print("Ambiente configurado com sucesso!")
print("---------------------------------")
print(f"Nome fictício gerado: {fake.name()}")
print(f"CPF fictício gerado: {fake.cpf()}")
print(f"Cidade fictícia gerada: {fake.city()}")