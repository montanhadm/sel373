from flask import Flask, render_template, request, session, escape, redirect, url_for
from passlib.hash import pbkdf2_sha256
import sqlite3 as sql
from datetime import datetime

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
			return render_template('index.html', error=error)
	else:
		if 'username' in session:
			return render_template('index.html', user=escape(session['username']))
		return render_template('index.html')


@app.route('/logout/')
def logout():
	if 'username' in session:
		session.pop('username', None)
	return redirect('/')


@app.route('/add/', methods=['POST', 'GET'])
def new_leitura():
	if 'username' in session:

		now = datetime.now()
		time = "{:02d}:{:02d}".format(now.hour, now.minute)
		date = "{}-{:02d}-{:02d}".format(now.year, now.month, now.day)

		if request.method == 'POST':
			try:
				data = request.form['Data']
				hora = request.form['Hora']
				valor = request.form['Valor']
				user = session['username']

				with sql.connect("database/winput.db") as con:
					cur = con.cursor()

				cur.execute("""INSERT INTO leituras (DATA, HORA, VALOR, USER) VALUES (?,?,?,?)""", (data, hora, valor, user))

				con.commit()
				msg = 1

			except:
				con.rollback()
				msg = 2

			finally:
				con.close()
				return render_template('add_leitura.html', msg=msg, user=escape(session['username']), nowtime=time, nowdate=date)
			
		else:
			return render_template('add_leitura.html', user=escape(session['username']), nowtime=time, nowdate=date)

	else:
		return redirect('/')


@app.route('/signup/', methods=['POST', 'GET'])
def signup():
	if request.method == 'POST':
		try:
			username = request.form['log_user']
			password = request.form['pass_user']
			confirm_pass = request.form['pass_user_confirm']
			error_id = 1

			if len(username) > 16 or len(username) < 4:
				return render_template('signup.html', msg = 5)

			elif not str.isalnum(username):
				return render_template('signup.html', msg = 7)

			elif len(password) > 20 or len(password) < 4:
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

					return render_template('index.html', msg = 100)

				else:
					con.rollback()
					error_id = 8
					con.close()
					error_id = 9
					return render_template('signup.html', msg = 3) # usuario existente

			else:
				return render_template('signup.html', saved_user = username, msg = 2) # as senhas nao batem

		except:
			return render_template('signup.html', msg = 4, error_id = error_id) # erro ao conectar com SQL

	else:
		if 'username' in session:
			return redirect('/')
		else:
			return render_template('signup.html')

@app.route('/view/', methods=['GET'])
def visualizador():
	if 'username' in session:
		return redirect('/view/table')
	else:
		return redirect('/')

@app.route('/view/table/', methods=['GET', 'POST'])
def view_table():
	if 'username' in session:

		user = session['username']
		con = sql.connect("database/winput.db")
		con.row_factory = sql.Row
		cur = con.cursor()

		if request.method == 'GET':
			cur.execute("SELECT * FROM leituras WHERE USER = ? ORDER BY DATA DESC, HORA DESC", (user,))

			rows = cur.fetchall()

			return render_template('view_leitura.html', rows=rows, user=escape(session['username']))

		else:
			ano = request.form['ano']
			mes = request.form['mes']
			dia = request.form['dia']
			if ano != 'ano':
				if mes != 'mes':
					if dia != 'dia':
						search = "{:04d}-{:02d}-{:02d}".format(ano, mes, dia)
						cur.execute("SELECT * FROM leituras WHERE DATA = ? ORDER BY DATA DESC, HORA DESC", (search,))
					else:
						search = "{:04d}-{:02d}".format(ano,mes)
						cur.execute("SELECT * FROM leituras WHERE SUBSTR(DATA,1,7) = ? ORDER BY DATA DESC, HORA DESC", (search,))
				else:
					search = "{:04d}".format(ano)
					cur.execute("SELECT * FROM leituras WHERE SUBSTR(DATA,1,4) = ? ORDER BY DATA DESC, HORA DESC", (search,))
			else:
				cur.execute("SELECT * FROM leituras WHERE USER = ? ORDER BY DATA DESC, HORA DESC", (user,))

			rows = cur.fetchall()
			return render_template('view_leitura.html', rows=rows, user=escape(session['username']))
	else:
		return redirect('/')


@app.route('/view/chart/', methods=['GET'])
def view_chart():
	if 'username' in session:
		return redirect('/view/table')
	else:
		return redirect('/')

@app.route('/remove/<int:row_id>')
def remove_row(row_id):
	if 'username' in session:
		user = session['username']
		con = sql.connect("database/winput.db")
		cur = con.cursor()
		cur.execute("SELECT * FROM leituras WHERE ID = ?", (row_id,))
		row = cur.fetchone()

		if row[3] == user:
			cur.execute("DELETE FROM leituras WHERE ID = ?", (row_id,))
			con.commit()
			con.close()
			return redirect('/view/table/')

		else:
			con.close()
			return redirect('/view/table/')

	else: 
		return redirect('/')

@app.route('/view/estimate/', methods=['GET'])
def view_estimate():
	if 'username' in session:
		return redirect('/view/table')
	else:
		return redirect('/')
		

@app.route('/view/statistics/', methods=['GET'])
def view_statistics():
	if 'username' in session:
		return redirect('/view/table')
	else:
		return redirect('/')

@app.route('/torugo/', methods=['GET'])
def add_photo():
	return render_template('add_photo.html')


@app.errorhandler(404)
def page_not_found():
    return redirect('/')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="80")