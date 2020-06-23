import pyrebase
from datetime import datetime

from django.shortcuts import render, redirect
from django.contrib import auth, sessions

config = {
	'apiKey': "AIzaSyBLVuFlaifTPkHpHO1LPo6nAmNvyjS06sc",
  	'authDomain': "django-test-5c33d.firebaseapp.com",
  	'databaseURL': "https://django-test-5c33d.firebaseio.com",
  	'projectId': "django-test-5c33d",
  	'storageBucket': "django-test-5c33d.appspot.com",
  	'messagingSenderId': "971626209869",
  	'appId': "1:971626209869:web:2905f46d3f5810fc2ef204"
}

firebase     = pyrebase.initialize_app(config)
fireauth     = firebase.auth()
database     = firebase.database()

def sign_in(request):
	return render(request, 'sign_in.html')


def post_sign(request):
	email = request.POST.get('email')
	password = request.POST.get('password')

	try:
		user = fireauth.sign_in_with_email_and_password(email, password)
	except Exception as e:
		message = "Invalid Credentials"
		print(e)
		return render(request, 'sign_in.html', {'msg': message})
	session_id = user['localId']
	request.session['uid'] = str(session_id)
	request.session['email'] = str(email)
	return render(request, 'welcome.html', {"email": email})


def logout(request):
	auth.logout(request)
	return render(request, 'sign_in.html')


def password_reset_view(request):
	return render(request, 'password_reset_form.html')


def password_reset_sent(request):
	try:
		email = request.POST.get('email')
		user = fireauth.send_password_reset_email(email)
	except Exception as e:
		message = "Please enter your email"
		print(e)
		return render(request, 'password_reset_form.html', {'msg': message})
	return render(request, 'password_reset_sent.html')


def signup(request):
	if request.method == 'POST':
		try:
			name = request.POST.get('name')
			email = request.POST.get('email')
			password = request.POST.get('password')
			user = fireauth.create_user_with_email_and_password(email, password)
			uid = user['localId']
			data = {'name': name, 'status': 1}
			database.child("users").child(uid).child("details").set(data)
			return redirect('sign_in')
		except Exception as e:
			message = "Unable to create account. Please Try again"
			print(e)
			return redirect('sign_in')
	else:
		return render(request, 'sign_up.html')

def callback(request):
	if request.method == 'POST':
		try:
			phone = request.POST.get('phone')
			user = request.session['uid']
			data = {'phone': phone, 'status': 'active'}
			database.child("callback").child(user).set(data)
			return render(request, 'welcome.html', {"email": request.session['email']})
		except Exception as e:
			message = "Unable to create callback. Please Try again"
			print(e)
			return render(request, 'welcome.html', {"email": request.session['email']})
	else:
		return render(request, 'callback.html')

def order(request):
	if request.method == 'POST':
		try:
			registration_id = str(request.POST.get('registration_id'))
			phone           = str(request.POST.get('phone'))
			positions       = str(request.POST.get('positions'))
			date_now        = str(datetime.now())
			order_id        = str(database.child('order_counter').get().val())
			order_counter   = str(int(order_id) + 1)
			user            = request.session['uid']
			data            = {'OrderID': order_id, 'registration_id': registration_id, 'phone': phone, 'positions': positions, 'date': date_now, 'status': 'active'}
			database.child("orders").child(user).set(data)
			database.child('order_counter').set(order_counter)
			return render(request, 'welcome.html', {"email": request.session['email']})
		except Exception as e:
			message = "Unable to create callback. Please Try again"
			print(e)
			return render(request, 'welcome.html', {"email": request.session['email']})
	else:
		return render(request, 'order.html')