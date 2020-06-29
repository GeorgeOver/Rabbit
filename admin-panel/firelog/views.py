import pyrebase
from datetime import datetime

from django.shortcuts import render, redirect
from django.contrib import auth, sessions

config = {
	'apiKey': "AIzaSyB5Kr4pKwoCuvVoJWdgyTuPwTWnS4j2d08",
    'authDomain': "krolchansk-fdea7.firebaseapp.com",
    'databaseURL': "https://krolchansk-fdea7.firebaseio.com",
    'projectId': "krolchansk-fdea7",
    'storageBucket': "krolchansk-fdea7.appspot.com",
    'messagingSenderId': "808335114604",
    'appId': "1:808335114604:web:b37444b60e5194da1df349"
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


def get_data_from_database():
	active_orders = database.child('active_orders').shallow().get().val()
	active_orders_list = []
	for element in active_orders:
		active_orders_list.append(element)

	registration_ids = []
	customer_names   = []
	emails           = []
	phones           = []
	dates            = []
	positions        = []
	statuses         = []

	for order in active_orders_list:
		registration_ids.append(database.child('active_orders').child(order).child('registration_id').get().val())
		customer_names.append(database.child('active_orders').child(order).child('name').get().val())
		emails.append(database.child('active_orders').child(order).child('email').get().val())
		phones.append(database.child('active_orders').child(order).child('phone').get().val())
		"""
		position = database.child('active_orders').child(order).child('positions').get().val().split('[')[1].split(']')[0].split(',')
		new_pos = ''
		for pos in position:
			splitted_pos = pos.split('  ')
			new_pos = new_pos + splitted_pos[0] + ' ' + splitted_pos[1] + ' шт. ' + splitted_pos[2] + ' Руб.;\n'
		positions.append(new_pos)
		"""
		positions.append(database.child('active_orders').child(order).child('positions').get().val())
		status = database.child('active_orders').child(order).child('status').get().val()
		if status == '0':
			status = 'Ожидает принятия'
		elif status == '1':
			status = 'Принят'
		elif status == '2':
			status = 'Отклонен'
		elif status == '3':
			status = 'Собран и ожидает отправки'
		elif status == '4':
			status = 'Отправлен'
		elif status == '5':
			status = 'Доставлен'
		elif status == '6':
			status = 'Завершен'
		statuses.append(status)

	comb = zip(active_orders_list, registration_ids, customer_names, emails, phones, positions, statuses)

	return comb


def get_callbacks_from_database():
	callback = database.child('callback').shallow().get().val()
	callback_list = []
	for element in callback:
		callback_list.append(element)

	phones           = []
	statuses         = []

	for cb in callback_list:
		phones.append(database.child('callback').child(cb).child('phone').get().val())
		status = database.child('callback').child(cb).child('status').get().val()
		if status == '0':
			status = 'Активен'
		elif status == '1':
			status = 'Завершен'
		elif status == '2':
			status = 'Не удалось дозвониться'
		statuses.append(status)

	cb_comb = zip(callback_list, phones, statuses)

	return cb_comb


def get_prices_from_database():
	prices_ids = database.child('prices').shallow().get().val()
	prices_ids_list = []
	for element in prices_ids:
		prices_ids_list.append(int(element))

	prices_ids_list.sort()

	for prices_id in prices_ids_list:
		prices_id = str(prices_id)

	names           = []
	prices          = []
	measures        = []

	for price_id in prices_ids_list:
		names.append(database.child('prices').child(price_id).child('name').get().val())
		prices.append(database.child('prices').child(price_id).child('price').get().val())
		measures.append(database.child('prices').child(price_id).child('measure').get().val())

	price_comb = zip(prices_ids_list, names, prices, measures)

	return price_comb


def manage(request):
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

	comb       = get_data_from_database()
	cb_comb    = get_callbacks_from_database()
	price_comb = get_prices_from_database()

	return render(request, 'manage.html', {"email": email, "comb": comb, 'cb_comb': cb_comb, 'price_comb': price_comb})


def change_status(request):
	data = str(request.GET.get('data')).split('___')
	order = data[0]
	reg_id = data[1]
	return render(request, 'change_status.html', {'order': order, 'reg_id': reg_id})


def change_position(request):
	data = str(request.GET.get('data')).split('___')
	item_id  = data[0]
	name     = data[1]
	price    = data[2]
	measure  = data[3]
	return render(request, 'change_position.html', {'item_id': item_id, 'name': name, 'price': price, 'measure': measure})


def post_change_status(request):
	order = request.POST.get('order')
	new_status = request.POST.get('status')
	reg_id = request.POST.get('reg_id')
	database.child('active_orders').child(order).child('status').set(new_status)
	if new_status == '0':
		new_status = 'Ожидает принятия'
	elif new_status == '1':
		new_status = 'Принят'
	elif new_status == '2':
		new_status = 'Отклонен'
	elif new_status == '3':
		new_status = 'Собран и ожидает отправки'
	elif new_status == '4':
		new_status = 'Отправлен'
	elif new_status == '5':
		new_status = 'Доставлен'
	elif new_status == '6':
		new_status = 'Завершен'

	push_notify(order, new_status, reg_id)

	comb       = get_data_from_database()
	cb_comb    = get_callbacks_from_database()
	price_comb = get_prices_from_database()

	return render(request, 'manage.html', {"comb": comb, 'cb_comb': cb_comb, 'price_comb': price_comb})


def post_change_position(request):
	item_id = request.POST.get('item_id')
	name    = request.POST.get('name')
	price   = request.POST.get('price')
	measure = request.POST.get('measure')
	database.child('prices').child(item_id).child('name').set(name)
	database.child('prices').child(item_id).child('price').set(price)
	database.child('prices').child(item_id).child('measure').set(measure)
	
	comb       = get_data_from_database()
	cb_comb    = get_callbacks_from_database()
	price_comb = get_prices_from_database()

	return render(request, 'manage.html', {"comb": comb, 'cb_comb': cb_comb, 'price_comb': price_comb})


def change_callback(request):
	callback = str(request.GET.get('callback'))
	return render(request, 'change_callback.html', {'callback': callback})


def post_change_callback(request):
	callback = request.POST.get('callback')
	new_status = request.POST.get('status')
	database.child('callback').child(callback).child('status').set(new_status)

	comb       = get_data_from_database()
	cb_comb    = get_callbacks_from_database()
	price_comb = get_prices_from_database()

	return render(request, 'manage.html', {"comb": comb, 'cb_comb': cb_comb, 'price_comb': price_comb})


def delete_order(request):
	order = str(request.GET.get('order'))
	database.child('active_orders').child(order).remove()
	
	comb       = get_data_from_database()
	cb_comb    = get_callbacks_from_database()
	price_comb = get_prices_from_database()

	return render(request, 'manage.html', {"comb": comb, 'cb_comb': cb_comb, 'price_comb': price_comb})


def delete_position(request):
	item_id = str(request.GET.get('id'))
	database.child('prices').child(item_id).remove()
	
	comb       = get_data_from_database()
	cb_comb    = get_callbacks_from_database()
	price_comb = get_prices_from_database()

	return render(request, 'manage.html', {"comb": comb, 'cb_comb': cb_comb, 'price_comb': price_comb})


def delete_callback(request):
	callback = str(request.GET.get('callback'))
	database.child('callback').child(callback).remove()
	
	comb       = get_data_from_database()
	cb_comb    = get_callbacks_from_database()
	price_comb = get_prices_from_database()

	return render(request, 'manage.html', {"comb": comb, 'cb_comb': cb_comb, 'price_comb': price_comb})

def push_notify(order_id, status, reg_id):
	import requests
	import json

	serverToken = 'AAAAvDSHAWw:APA91bHLFq2FUoob9yIJCxJVf2b2n4hE0lk8kAPEuN6OhAkPlfjfFAAImlZdp9EkmmtH-7nDg6dUzw0Dq2A4emkead6nj3Sdh8FdtM5bTDpMMir1W_vdgpC4lLvfKrwpO6V3z2mrQg1m'
	#deviceToken = 'dL6wrJnT5z5DoQpvzeV9qG:APA91bH8DEhWcU5tFzKOkrwRC84ZFfy2MLzR70_J5kEnWvZR298UIJFuRIFNZg98fBq-uEnWJJwPVZZ--BtRMFK7S3XRLe5woUyb4hu50vmgmj7jCa8PZSD_iuitZGBc6oUcb7Ut5_61'
	deviceToken = reg_id
	"""
	if deviceToken == reg_id:
		print('SUCCESS')
	"""

	headers = {
	        'Content-Type': 'application/json',
	        'Authorization': 'key=' + serverToken,
	      }

	body = {
	          'notification': {'title': "Заказ " + str(order_id),
	                            'body': "Статус изменен: " + str(status)
	                            },
	          'to':
	              deviceToken,
	          'priority': 'high',
	        }
	response = requests.post("https://fcm.googleapis.com/fcm/send",headers = headers, data=json.dumps(body))
	print(response.status_code)

	print(response.json())