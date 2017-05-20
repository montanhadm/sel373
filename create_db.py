import sqlite3

conn = sqlite3.connect('database/wtable.db')
print("Database aberta com sucesso")

#conn.execute('CREATE TABLE users (USER TEXT, PASS TEXT, GENDER TEXT)')
#print("Tabela de usuários criada com sucesso")
conn.close()