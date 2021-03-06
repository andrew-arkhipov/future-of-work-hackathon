from app import app
from flask import render_template, request, flash
import neural_net
import random

import pyrebase

config = {
    "apiKey": "AIzaSyA9ztSjoWR9ZJrX5o8VaJacyika26-xxkg",
    "authDomain": "fuelforthought-fb7ed.firebaseapp.com",
    "databaseURL": "https://fuelforthought-fb7ed.firebaseio.com",
    "projectId": "fuelforthought-fb7ed",
    "storageBucket": "fuelforthought-fb7ed.appspot.com",
    "messagingSenderId": "622592343203",
    "appId": "1:622592343203:web:33aef1692ca30630731316"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

@app.route('/index')
@app.route('/')
def index():
	return render_template('main.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		email = request.form['email']
		password = request.form['pw']
		if request.form["action"] == "login":
			try:
				auth.sign_in_with_email_and_password(email, password)
				name = request.cookies.get('name')
				location = request.cookies.get('location')
				occupation = request.cookies.get('occupation')
				return render_template('dashboard.html', name=name, location=location, occupation=occupation)
			except:
				return 'Login failed'
		elif request.form["action"] == "signup":
			try:
				user = auth.create_user_with_email_and_password(email, password)
				if (user):
					print(user['idToken'])
					return render_template('question.html')
				else:
					print(user['error']['message'])
			except Exception as e:
				print("ERROR")
				print(type(e))
				# print(user)

			return render_template('main.html')
		else:
			assert(0)

@app.route('/assessment')
def assessment():
	return render_template('question.html')

@app.route('/assessment2')
def assessment2():
	return render_template('question_two.html')

@app.route('/assessment3')
def assessment3():
	return render_template('question_three.html')

@app.route('/assessment4')
def assessment4():
	return render_template('question_four.html')

@app.route('/assessment5')
def assessment5():
	return render_template('question_five.html')

@app.route('/algo')
def algo():
	question_list = [float(request.cookies.get(f"question{i}")) for i in range(1,6)]
	print(question_list)
	answer = neural_net.model(question_list)

	type_dic = {key:value for key,value in zip(['Type 1', 'Type 2', 'Type3 3', 'Type 4'], 'Creative Efficient Extrovert Free-Thinking'.split(' '))}

	result_dic = {key:value for key,value in zip('Creative Efficient Extrovert Free-Thinking'.split(' '), ['Efficient, Secure, Free-Thinking', 'Introvert, Compassionate, Secure',
																											 'Easy-Going, Consistent, Sensitive', 'Creative, Efficient, Consistent'])}
	
	time = request.cookies.get('time')

	return render_template('algo.html', neural_score=answer, personality=type_dic[answer], result=result_dic[type_dic[answer]], time=time)

@app.route('/dashboard')
def dashboard():
	name = request.cookies.get('name')
	location = request.cookies.get('location')
	occupation = request.cookies.get('occupation')
	return render_template('dashboard.html', name=name, location=location, occupation=occupation)

@app.route('/game')
def game():
	return render_template('game.html')


