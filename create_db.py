import sqlite3

conn = sqlite3.connect('database/database.db')
print("Database aberta com sucesso")

conn.execute('CREATE TABLE leituras (DATA TEXT, HORA TEXT, VALOR INTEGER)')
print("Tabela de leituras criada com sucesso")
conn.close()