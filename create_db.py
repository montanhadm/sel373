import sqlite3

conn = sqlite3.connect('database/users.db')
print("Database aberta com sucesso")

conn.execute('CREATE TABLE users (USER TEXT, PASS TEXT, GENDER TEXT)')
print("Tabela de usuários criada com sucesso")
conn.commit()
conn.close()