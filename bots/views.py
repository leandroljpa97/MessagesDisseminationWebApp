import requests, json, time

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.core.serializers import serialize

from django.utils.timezone import now

from management.models import Buildings, Users, LogsMovements, Messages, Bots

from pprint import pprint

# Create your views here.

def sendMessages(request):
	counter = 1

	if request.method == 'POST':
		
		_bot_id = request.POST.get('bot_id', '')
		_password = request.POST.get('password', '')

		#print('Bot ID: ' + _bot_id)
		#print('Building ID: ' + _build_id)
		#print('Password: ' + _password + '\n')
		aux = Bots.objects.filter(id = _bot_id, password = _password)

		if not aux:
			return HttpResponse("Error: Invalid Arguments", content_type = "text/plain", status = 400)

		_content = request.POST.get('message', '')
		if not _content:
			return HttpResponse("Error: Empty Message", content_type = "text/plain", status = 400)

		_number = request.POST.get('number', '')
		if not _number:
			_number = '1'

		_periodicity = request.POST.get('periodicity', '')
		if not _periodicity:
			_periodicity = '0'

		for item in aux:
			_build_id = item.build_id


		while True:
			_allUsers = Users.objects.filter(build_id = _build_id)
			if not _allUsers:
				return HttpResponse("Error: No Users in that Building", content_type = "text/plain", status = 400)

			for item in _allUsers:
				_message = Messages(content = _content, receiver = item, date = now(), sender = "BOT : " + _bot_id, build_id = _build_id)
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
