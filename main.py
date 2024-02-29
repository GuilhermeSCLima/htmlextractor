from extract import extract
from sql import sql

print("""
Escolha qual opção deseja:
[1] = Busque os dados
[2] = Gerar arquivo SQL
[0] = Sair
""")

choose = int(input("Selecione:\n"))

if choose == 0:
    exit()
elif choose == 1:
    extract()
elif choose == 2:
    sql()