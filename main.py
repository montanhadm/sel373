from flask import Flask, render_template, request, session, escape, redirect, url_for
import sqlite3 as sql

app = Flask(__name__)
app.secret_key = 'SysfCK;U{2~e*\yn!w$%'

@app.route('/', methods=['POST', 'GET'])
def index():
	if request.method == 'POST':
		try:
			session['username'] = request.form['log_user']
			return redirect('/add/')
			# Tratar se login existe e se senha está correta
		except:
			# Tratar exceção
			return render_template('index.html')
	else:
		if 'username' in session:
			return render_template('index.html', user=escape(session['username']))
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
			if 'username' in session:
				return render_template('add_leitura.html', msg=msg, user=escape(session['username']))
			return render_template('add_leitura.html', msg=msg)
			
	else:
		return render_template('add_leitura.html', msg=msg, user=escape(session['username']))


@app.route('/signup/')
def signup():
	if 'username' in session:
		return redirect(url_for('/'))
	else:
		return render_template('signup.html')


@app.route('/view/', methods=['GET'])
def view_leitura():
	con = sql.connect("database/database.db")
	con.row_factory = sql.Row

	cur = con.cursor()
	cur.execute("select * from leituras")

	rows = cur.fetchall()

	if 'username' in session:
		return render_template('view_leitura.html', rows=rows, user=escape(session['username']))
	return render_template('view_leitura.html', rows=rows)


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")