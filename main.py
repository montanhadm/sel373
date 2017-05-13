from flask import Flask, render_template, request
import sqlite3 as sql

app = Flask(__name__)


@app.route('/')
def index():
	return render_template('index.html')


@app.route('/add/', methods=['POST', 'GET'])
def new_leitura():
	if request.method == 'POST':
		try:
			data = request.form['Data']
			hora = request.form['Hora']
			valor = request.form['Valor']

			with sql.connect("database/database.db") as con:
				cur = con.cursor()

			cur.execute("""INSERT INTO leituras (DATA, HORA, VALOR) VALUES (?,?,?)""", (data, hora, valor))

			con.commit()
			msg = 1

		except:
			con.rollback()
			msg = 2

		finally:
			con.close()
			return render_template('add_leitura.html', msg=msg)
			
	else:
		return render_template('add_leitura.html')


@app.route('/view/', methods=['GET'])
def view_leitura():
	con = sql.connect("database/database.db")
	con.row_factory = sql.Row

	cur = con.cursor()
	cur.execute("select * from leituras")

	rows = cur.fetchall()
	return render_template('view_leitura.html', rows=rows)


if __name__ == '__main__':
    app.run(debug=True)