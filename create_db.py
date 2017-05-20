import sqlite3

conn = sqlite3.connect('database/winput.db')
print("Database aberta com sucesso")

conn.execute('CREATE TABLE leituras (VALOR INTEGER, DATA TEXT, HORA TEXT, USER TEXT)')
print("Tabela de usuários criada com sucesso")
conn.close()