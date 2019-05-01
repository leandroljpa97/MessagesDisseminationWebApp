from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.core.serializers import serialize
from management.models import Buildings, Users, LogsMovements, Messages
from math import sin, cos, sqrt, atan2, radians
from django.db.models import Count, Q
import fenixedu
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
import requests
from django.utils.timezone import now


# para a cache
from django.utils.decorators import method_decorator
from django.core.cache import cache




import json
import os
import string

from django.db import connection
from django.conf import settings
from django.utils import timezone

from MessagesDisseminationWebApp.settings import redirect_uri, client_id, secret




request_url = 'https://fenix.tecnico.ulisboa.pt/oauth/userdialog?client_id=' + client_id + '&redirect_uri=' + redirect_uri

def index(request):
	access_token=request.COOKIES.get('token')
	#print("o accesssss é...?")
	#print(access_token)
	if access_token==None:
		nr={}
		nr['flag']=0
		context ={'user':nr}
		response = render(request, './userInterface.html',context)

	else:
		_ist_id=cache.get(access_token,-1)

		#_name= cache.get(access_token+_ist_id,'ui');
		nr={}
		if _ist_id == -1:
			nr['flag']=0
		else:
			_name = cache.get(access_token+_ist_id,'ui')
			nr['flag']=1
			nr['ist_id']=_ist_id
			nr['name']=_name
		context ={'user':nr}
		response = render(request, './userInterface.html',context)
		if _ist_id==-1:
			response.delete_cookie('token')
	return response



def auxiliar(request):

	_m= Messages(content='xxx', receiver='ist425412', sender='ist423333', date= now(), build_id= -1)
	_m.save()
	_m1= Messages(content='yyy', receiver='ist42553', sender='ist425412', date= now(), build_id= -1)
	_m1.save()
	
	return HttpResponse('<p>FUNCAO AUXILIAR </p>')


def login(request):
	return redirect(request_url)



def auth(request):
	code = request.GET.get('code')
	access_token_request_url = 'https://fenix.tecnico.ulisboa.pt/oauth/access_token'
	_data = {'client_id': client_id, 'client_secret': secret,'redirect_uri': redirect_uri, 'code': code, 'grant_type': 'authorization_code'}
	
	request_access_token = requests.post(access_token_request_url, data=_data)


	if request_access_token.status_code != 200 or 'error' in request_access_token.json():
		return render(request, './invalid.html')
	else:
		access_token = request_access_token.json().get('access_token')
		#print("acess_token no login")
		#print(access_token)
		refresh_token = request_access_token.json().get('refresh_token')
		token_expires = request_access_token.json().get('expires_in')

		params = {'access_token': access_token}
		request_info = requests.get('https://fenix.tecnico.ulisboa.pt/api/fenix/v1/person', params=params)
		_ist_id = request_info.json().get('username')
		_name = request_info.json().get('name')

		y=cache.set(access_token,_ist_id,60*60)
		z=cache.set(access_token+_ist_id,_name,60*60)
		


		if not Users.objects.filter(ist_id =_ist_id).exists():
			_user= Users(ist_id = _ist_id, name= _name, build_id='1', range_user = 100, lat=38.7368263, longit= -9.1392)
			_user.save()

		# response = render(request, './userInterface.html',context)
		response= redirect('users:home')
		response.set_cookie('token', access_token)
		return response

def logout(request):
	access_token=request.COOKIES.get('token')
	ist_id=cache.get(access_token,-1)
	if ist_id==-1:
		response= redirect('users:home')
		response.delete_cookie('token')
		return response
	else:
		response = render(request, './GoodBye.html')
		if request.method=='POST':
			cache.delete(access_token)
			cache.delete(access_token+ist_id)
			if request.COOKIES.get('token'):
				response.delete_cookie('token')
			Users.objects.filter(ist_id=ist_id).delete()
			#print('dentro do logout-> a cache é')
			#print(cache.get('id'))
			return response



def range(request):
	access_token=request.COOKIES.get('token')
	ist_id=cache.get(access_token,-1)
	if ist_id==-1:
		response= redirect('users:home')
		response.delete_cookie('token')
		return response
	else:
		if request.method == 'POST':
			_range= request.POST.get('range', '')
			Users.objects.filter(ist_id=ist_id).update(range_user = _range)
			return HttpResponse(status=204)
	return HttpResponse('<p>Nothing to show</p>')		


def checkDistance(_lat1,_lat2,_long1,_long2,_range):
	R = 6373.0

	lat1 = radians(_lat1)
	lon1 = radians(_long1)
	lat2 = radians(_lat2)
	lon2 = radians(_long2)

	dlon = lon2 - lon1
	dlat = lat2 - lat1

	a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
	c = 2 * atan2(sqrt(a), sqrt(1 - a))

	_distance = R * c * 1000
	if _distance <_range:
		return 1
	return 0


def nearbyRange(request):
	access_token=request.COOKIES.get('token')
	ist_id=cache.get(access_token,-1)
	if ist_id==-1:
		response= redirect('users:home')
		response.delete_cookie('token')
		return response
	else:
		_data= Users.objects.filter(ist_id=ist_id)
		for aux in _data:
			_range=aux.range_user
			_lat=aux.lat
			_longit=aux.longit
		# Q is to exclude the user with this ist_id
		_allUsers=Users.objects.all().filter(~Q(ist_id=ist_id))

		nearMe=[]
		for item in _allUsers:
			if checkDistance(item.lat,_lat,item.longit,_longit,_range)==1:
				nearMe.append({'ist_id':item.ist_id})

		if len(nearMe)>0:
			return HttpResponse(nearMe, content_type = 'application/json')
		else:
			return HttpResponse("<h3> No one in your range </h3>")
	


def nearbyBuilding(request):
	access_token=request.COOKIES.get('token')
	ist_id=cache.get(access_token,-1)
	if ist_id==-1:
		response= redirect('users:home')
		response.delete_cookie('token')
		return response
	else:
		_me=Users.objects.filter(ist_id=ist_id)
		for aux in _me:
			_users=Users.objects.filter(build_id=aux.build_id).filter(~Q(ist_id=ist_id))
			if aux.build_id == '-1':
				return HttpResponse("<h3> You are not in any building </h3>")
			else:
				_allUsers=[]
				for item in _users:
					_allUsers.append({'ist_id':item.ist_id})

		return HttpResponse(_allUsers, content_type = 'application/json')
	

# @login_required(login_url='users:home')
def sendMessage(request):
	access_token=request.COOKIES.get('token')
	ist_id=cache.get(access_token,-1)
	if ist_id==-1:
		response= redirect('users:home')
		response.delete_cookie('token')
		return response
	else:
		if request.method == 'POST':
			_content=request.POST.get('message', '')
			_data= Users.objects.filter(ist_id=ist_id)
			for aux in _data:
				_range=aux.range_user
				_lat=aux.lat
				_longit=aux.longit
		# Q is to exclude the user with this ist_id
			_allUsers=Users.objects.all().filter(~Q(ist_id=ist_id))

			for item in _allUsers:
				if checkDistance(item.lat,_lat,item.longit,_longit,_range)==1:
					_message=Messages(content=_content,receiver=item.ist_id,date=now(),sender=ist_id, build_id=item.build_id)
					_message.save()
			return HttpResponse(status=204)
		else:	
			allMessages=Messages.objects.all()
			response = serialize("json", allMessages)
			return HttpResponse(response, content_type = 'application/json')


def sendMessageBuild(request):
	access_token=request.COOKIES.get('token')
	ist_id=cache.get(access_token,-1)
	if ist_id==-1:
		response= redirect('users:home')
		response.delete_cookie('token')
		return response
	else:
		if request.method == 'POST':
			_content=request.POST.get('message', '')
			_data= Users.objects.filter(ist_id=ist_id)
			for aux in _data:
				_build_id=aux.build_id
				#print("my_build_id")
				#print(_build_id)
			if (_build_id!= -1):
			# Q is to exclude the user with this ist_id
				_allUsers=Users.objects.all().filter(~Q(ist_id=ist_id))

				for item in _allUsers:
					if item.build_id==_build_id:
						_message=Messages(content=_content,receiver=item.ist_id,date=now(),sender=ist_id, build_id=item.build_id)
						_message.save()
			return HttpResponse(status=204)
				
		allMessages=Messages.objects.all()
		response = serialize("json", allMessages)
		return HttpResponse(response, content_type = 'application/json')


def checkBuilding(_latUser,_longitUser):
	#verificar qual o raio a meter
	radius=70
	allBuilds=Buildings.objects.all()
	for item in allBuilds:
		if checkDistance(_latUser,item.lat,_longitUser,item.longit,radius)==1:
			return item.id
	return -1
	

def updateLocation(request):
	access_token=request.COOKIES.get('token')
	_ist_id=cache.get(access_token,-1)
	if _ist_id == -1:
		response= redirect('users:home')
		response.delete_cookie('token')
		return response
	else:
		if request.method =='POST':
			_lat=request.POST.get('lat')
			_lat= float(_lat)
			_longit=request.POST.get('longit')
			_longit=float(_longit)
			_build_id = checkBuilding(_lat,_longit)

			#print('longit')
			#print(_longit)
			#print('latittt')
			#print(_lat)

			_user =  Users.objects.filter(ist_id = _ist_id)

			for item in _user:
				if _build_id == item.build_id:
					Users.objects.filter(ist_id=_ist_id).update(lat = _lat, longit = _longit)
				else:
					Users.objects.filter(ist_id = _ist_id).update(lat = _lat, longit = _longit, build_id = _build_id)
					if not LogsMovements.objects.filter(ist_id = _ist_id):
						if _build_id != -1:
							_logs = LogsMovements(ist_id = _ist_id, build_id = _build_id, start = now())
							_logs.save()
					else:
						LogsMovements.objects.filter(ist_id = _ist_id).filter(build_id = item.build_id).update(end = now())
						if _build_id != -1:
							_logs = LogsMovements(ist_id = _ist_id, build_id = _build_id, start = now())
							_logs.save()

			return HttpResponse(status=204)
	return HttpResponse('<p>Nothing to show</p>')	


def getMessages(request):
	access_token=request.COOKIES.get('token')
	_ist_id=cache.get(access_token,-1)
	if _ist_id == -1:
		response= redirect('users:home')
		response.delete_cookie('token')
		return response
	else:
		if request.method=='GET':
			allMessages=Messages.objects.filter(receiver=_ist_id)

			messages= []
			for item in allMessages:
				messages.insert(0,{'date':item.date, 'content':item.content, 'sender':item.sender})

		return JsonResponse({'messages':messages})

def updateBuilding(request):
	access_token=request.COOKIES.get('token')
	_ist_id=cache.get(access_token,-1)
	if _ist_id == -1:
		response= redirect('users:home')
		response.delete_cookie('token')
		return response
	else:
		if request.method=='GET':
			_user=Users.objects.filter(ist_id=_ist_id)

			nr=[]
			for item in _user:
				#print("buildid")
				#print(item.build_id)
				_build_id=item.build_id
				#print(_build_id)
				#print(type(_build_id))

			if int(_build_id) == -1:
				build_name='You are not in any building'
			else:
				_build=Buildings.objects.filter(id=_build_id)

				for item in _build:
					build_name=item.name
			
			#print("o builllllllllllllllllllllddddddddd")
			#print(build_name)

			return JsonResponse({'build':build_name})









