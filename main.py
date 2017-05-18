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
		if 'username' in session:
			return render_template('add_leitura.html', user=escape(session['username']))
		return render_template('add_leitura.html')


@app.route('/signup/', methods=['POST', 'GET'])
def signup():
	if request.method == 'POST':
		try:
			username = request.form['log_user']
			password = request.form['pass_user']
			confirm_pass = request.form['pass_user_confirm']

			if password == confirm_pass:
				with sql.connect("database/users.db") as con:
					cur = con.cursor()

				cur.execute("""SELECT 1 FROM users WHERE USER = ?""", (username))
				data = cur.fetchone()
				if data is None:
					encrypt_pass = password
					cur.execute("""INSERT INTO users (USER, PASS, GENDER) VALUES (?,?,?)""", (username, encrypt_pass, 'M'))
					con.commit()
					con.close()
					return render_template('signup.html', msg = 1)

				else:
					con.rollback()
					con.close()
					return render_template('signup.html', msg = 3) # usuario existente

			else:
				return render_template('signup.html', saved_user = username, msg = 2) # as senhas não batem

		except:
			return render_template('signup.html', msg = 4) # erro ao conectar com SQL

	else:
		if 'username' in session:
			return redirect('/')
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


@app.errorhandler(404)
def page_not_found(e):
    return redirect('/'), 404


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")