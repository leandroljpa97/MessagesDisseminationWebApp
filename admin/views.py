import requests, json, random, time

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.core.serializers import serialize
from django.db.models import Q

# para a cache
from django.utils.decorators import method_decorator
from django.core.cache import cache

from django.utils.timezone import now

from management.models import Buildings, Users, LogsMovements, Messages, Bots

from pprint import pprint


# Create your views here.



	
def login_view(request):
	if request.method == 'POST':
		# Try to log user
		username = request.POST.get('username', '')
		password = request.POST.get('password', '')

		while True:
			secret = random.randint(1, 101)
			#print('Secret no login: ' + str(secret) + '\n')

			if cache.get(secret, -1) == -1:
				break

		if username == 'admin' and password == '123':
			#print('fiz login\n')

			cache.set(secret, 1, 60*60)

			#print('Cache no login: ' + str(cache.get(secret, -1)) + '\n')

			return JsonResponse({'secret': secret})
		else:
			return HttpResponse("Error: Invalid Login", content_type = "text/plain", status = 401)
	else:
		return HttpResponse("Error: Invalid Request", content_type = "text/plain", status = 400)

def check_authentication(request):
	secret = request.POST.get('secret', '')
	#print('Secret na autenticação: ' + str(secret) + '\n')

	if not secret:
		return 0

	#print('Cache na autenticação: ' + str(cache.get(secret, -1)) + '\n')

	if cache.get(secret, -1) == -1:
		return 0

	return secret

def buildings(request):
	if request.method == 'POST':
		if not check_authentication(request):
			return HttpResponse("Error: Invalid Login", content_type = "text/plain", status = 401)

		_id = request.POST.get('id', '')
		_name = request.POST.get('name', '')
		_lat = request.POST.get('lat', '')
		_longit = request.POST.get('longit', '')

		_building = Buildings(id = _id, name = _name, lat = _lat, longit = _longit)
		_building.save()

		return HttpResponse("Building Inserted", content_type = "text/plain")
	else:
		return HttpResponse("Error: Invalid Request", content_type = "text/plain", status = 400)

def users(request):
	if request.method == 'POST':
		if not check_authentication(request):
			return HttpResponse("Error: Invalid Login", content_type = "text/plain", status = 401)

		_users = Users.objects.all()
		response = serialize("json", _users)
		#pprint(response)
		return HttpResponse(response, content_type = 'application/json')
	else:
		return HttpResponse("Error: Invalid Request", content_type = "text/plain", status = 400)


def clear(request):
	if request.method == 'POST':
		if not check_authentication(request):
			return HttpResponse("Error: Invalid Login", content_type = "text/plain", status = 401)

		Buildings.objects.all().delete()
		Messages.objects.all().delete()
		LogsMovements.objects.all().delete()
		Bots.objects.all().delete()
		Users.objects.all().delete()

		return HttpResponse(response, content_type = 'application/json')
	else:
		return HttpResponse("Error: Invalid Request", content_type = "text/plain", status = 400)



def listUsersInBuilding(request):
	if request.method == 'POST':
		if not check_authentication(request):
			return HttpResponse("Error: Invalid Login", content_type = "text/plain", status = 401)

		_build_id = request.POST.get('build_id', '')
		if not Buildings.objects.filter(id = _build_id):
			return HttpResponse("Error: Invalid Building", content_type = "text/plain", status = 400)

		_users = Users.objects.filter(build_id = _build_id)
		response = serialize("json", _users)	
		return HttpResponse(response, content_type = 'application/json')
	else:
		return HttpResponse("Error: Invalid Request", content_type = "text/plain", status = 400)

import random, string

def randomword():
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for i in range(8))


def registerBot(request):
	if request.method == 'POST':
		if not check_authentication(request):
			return HttpResponse("Error: Invalid Login", content_type = "text/plain", status = 401)

		while True:
			_bot_id = random.randint(1, 101)
			#print('Bot ID: ' + str(_bot_id) + '\n')

			if not Bots.objects.filter(id = _bot_id):
				break

		_build_id = request.POST.get('build_id', '')
		if not Buildings.objects.filter(id = _build_id):
			return HttpResponse("Error: Invalid Building", content_type = "text/plain", status = 400)

		_password = randomword()

		_bots = Bots(id = _bot_id, build_id = _build_id, password = _password)
		_bots.save()

		return JsonResponse({'bot_id': _bot_id, 'build_id': _build_id, 'password': _password})
	else:
		return HttpResponse("Error: Invalid Request", content_type = "text/plain", status = 400)

def sendMessagesBot(request):
	counter = 1

	if request.method == 'POST':
		if not check_authentication(request):
			return HttpResponse("Error: Invalid Login", content_type = "text/plain", status = 401)

		_build_id = request.POST.get('build_id', '')
		if not Buildings.objects.filter(id = _build_id):
			return HttpResponse("Error: Invalid Building", content_type = "text/plain", status = 400)

		if not Bots.objects.filter(build_id = _build_id):
			return HttpResponse("Error: Don't exists Bot in that Building", content_type = "text/plain", status = 400)

		_content = request.POST.get('message', '')
		if not _content:
			return HttpResponse("Error: Empty Message", content_type = "text/plain", status = 400)

		_number = request.POST.get('number', '')
		if not _number:
			_number = '1'

		_periodicity = request.POST.get('periodicity', '')
		if not _periodicity:
			_periodicity = '0'

		while True:
			_allUsers = Users.objects.filter(build_id = _build_id)
			if not _allUsers:
				return HttpResponse("Error: No Users in that Building", content_type = "text/plain", status = 400)

			for item in _allUsers:
				_message = Messages(content = _content, receiver = item, date = now())
				_message.save()

			if counter == int(_number):
				break
			counter = counter + 1
			time.sleep(int(_periodicity))

		allMessages = Messages.objects.all()
		response = serialize("json", allMessages)

		#pprint(response)

		return HttpResponse("Bot Done", content_type = "text/plain")
	else:
		return HttpResponse("Error: Invalid Request", content_type = "text/plain", status = 400)

def logMovementsUser(request):
	if request.method == 'POST':
		if not check_authentication(request):
			return HttpResponse("Error: Invalid Login", content_type = "text/plain", status = 401)

		_ist_id = request.POST.get('ist_id', '')
		if not Users.objects.filter(ist_id = _ist_id):
			return HttpResponse("Error: Invalid User", content_type = "text/plain", status = 400)

		_logs = LogsMovements.objects.filter(ist_id = _ist_id)
		response = serialize("json", _logs)	
		return HttpResponse(response, content_type = 'application/json')
	else:
		return HttpResponse("Error: Invalid Request", content_type = "text/plain", status = 400)


def logMovementsBuilding(request):
	if request.method == 'POST':
		if not check_authentication(request):
			return HttpResponse("Error: Invalid Login", content_type = "text/plain", status = 401)

		_build_id = request.POST.get('build_id', '')
		if not Buildings.objects.filter(id = _build_id):
			return HttpResponse("Error: Invalid Building", content_type = "text/plain", status = 400)

		_logs = LogsMovements.objects.filter(build_id = _build_id)
		response = serialize("json", _logs)	
		return HttpResponse(response, content_type = 'application/json')
	else:
		return HttpResponse("Error: Invalid Request", content_type = "text/plain", status = 400)

def logMessagesUser(request):
	if request.method == 'POST':
		if not check_authentication(request):
			return HttpResponse("Error: Invalid Login", content_type = "text/plain", status = 401)

		_ist_id = request.POST.get('ist_id', '')
		if not Users.objects.filter(ist_id = _ist_id):
			return HttpResponse("Error: Invalid User", content_type = "text/plain", status = 400)

		_logs = Messages.objects.filter(Q(sender=_ist_id) | Q(receiver=_ist_id))
		response = serialize("json", _logs)	
		return HttpResponse(response, content_type = 'application/json')
	else:
		return HttpResponse("Error: Invalid Request", content_type = "text/plain", status = 400)

def logMessagesBuilding(request):
	if request.method == 'POST':
		if not check_authentication(request):
			return HttpResponse("Error: Invalid Login", content_type = "text/plain", status = 401)

		_build_id = request.POST.get('build_id', '')
		if not Buildings.objects.filter(id = _build_id):
			return HttpResponse("Error: Invalid Building", content_type = "text/plain", status = 400)

		_logs = Messages.objects.filter(build_id = _build_id)
		response = serialize("json", _logs)	
		return HttpResponse(response, content_type = 'application/json')
	else:
		return HttpResponse("Error: Invalid Request", content_type = "text/plain", status = 400)


def logout_view(request):
	if request.method == 'POST': 
		secret = check_authentication(request)

		if secret:
			#print(secret)
			cache.delete(secret)
			return HttpResponse("Logout Done", content_type = "text/plain")
		else:
			return HttpResponse("Error: Invalid Login", content_type = "text/plain", status = 401)
	else:
		return HttpResponse("Error: Invalid Request", content_type = "text/plain", status = 400)















def buildingsNum(request, num):
	_building=Buildings.objects.filter(id=num)
	response = serialize("json", _building)
	return HttpResponse(response, content_type = 'application/json')

def oneUser(request, ist_id):
	_user=Users.objects.filter(ist_id=ist_id)
	response = serialize("json", _user)
	return HttpResponse(response, content_type = 'application/json')


# from management.models import Buildings, Users
# Buildings.objects.all()
# build_x = Buildings.objects.get(name="Torre Norte")
# Users(ist_id = "ist425330", name = "Diogo Rodrigues", build_id = build_x, range_user = 100, lat = 38.7375584, longit = -9.1387255)
# Users.objects.all()
