from flask import Flask, render_template, request, session, escape, redirect, url_for
from passlib.hash import pbkdf2_sha256
import sqlite3 as sql

app = Flask(__name__)
app.secret_key = 'SysfCK;U{2~e*\yn!w$%'

@app.route('/', methods=['POST', 'GET'])
def index():
	if request.method == 'POST':
		try:
			username = request.form['log_user']
			password = request.form['pass_user']

			con = sql.connect("database/users.db")
			cur = con.cursor()
			cur.execute("SELECT PASS FROM users WHERE USER = ?", (username,))
			userdata = cur.fetchone()

			if userdata == None:
				return render_template('index.html', msg=1)

			error = 4

			if pbkdf2_sha256.verify(password, userdata[0]):
				error = 1
				session['username'] = username
				error = 2
				return redirect('/add/')

			else:
				error = 3
				return render_template('index.html', msg=2)

			# Tratar bruteforce!
		except:
			# Tratar exceção
			return render_template('index.html', error=error)
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
			error_id = 1

			if len(username) >= 16 or len(username) <= 4:
				return render_template('signup.html', msg = 5)

			elif not str.isalnum(username):
				return render_template('signup.html', msg = 7)

			elif len(password) >= 20 or len(password) <= 4:
				return render_template('signup.html', msg = 6) 

			elif password == confirm_pass:			
				with sql.connect("database/users.db") as con:
					cur = con.cursor()

				error_id = 2
				cur.execute("SELECT * FROM users WHERE USER = ?", (username,))
				error_id = 3

				if cur.fetchone() == None:
					encrypt_pass = pbkdf2_sha256.hash(password)
					error_id = 4
					cur.execute("""INSERT INTO users (USER, PASS, GENDER) VALUES (?,?,?)""", (username, encrypt_pass, 'M'))
					error_id = 5
					con.commit()
					con.close()

					#wcon = sql.connect("database/wtable.db")
					#wcur = wcon.cursor()
					#wcon.execute("CREATE TABLE"+username+"(VALOR INTEGER, DATA TEXT, HORA TEXT)")
					#wcon.close()

					return render_template('signup.html', msg = 1)

				else:
					con.rollback()
					error_id = 8
					con.close()
					error_id = 9
					return render_template('signup.html', msg = 3) # usuario existente

			else:
				return render_template('signup.html', saved_user = username, msg = 2) # as senhas não batem

		except:
			return render_template('signup.html', msg = 4, error_id = error_id) # erro ao conectar com SQL

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
	cur.execute("SELECT * FROM leituras")

	rows = cur.fetchall()

	if 'username' in session:
		return render_template('view_leitura.html', rows=rows, user=escape(session['username']))
	return render_template('view_leitura.html', rows=rows)


@app.errorhandler(404)
def page_not_found(e):
    return redirect('/'), 404


if __name__ == '__main__':
    app.run(host="0.0.0.0")