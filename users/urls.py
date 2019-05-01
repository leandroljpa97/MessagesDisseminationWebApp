from django.urls import path,include
from . import views
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_exempt

app_name='users'

urlpatterns = [
	path('', csrf_exempt(views.index), name = 'home'),
	path('auth/', csrf_exempt(views.auth), name = 'auth'),
	path('login/', csrf_exempt(views.login), name = 'login'),
	path('logout/', csrf_exempt(views.logout), name = 'logout'),
	#path('<str:ist_id>/messages/', csrf_exempt(views.messages), name = 'messages'),
    path('range/', csrf_exempt(views.range), name = 'range'),
    path('message/', csrf_exempt(views.sendMessage), name = 'sendMessage'),
    path('messageBuilding/', csrf_exempt(views.sendMessageBuild), name = 'sendMessageBuild'),
    path('users/range/', csrf_exempt(views.nearbyRange), name = 'nearbyRange'),
    path('users/building/', csrf_exempt(views.nearbyBuilding), name = 'nearbyBuilding'),
    path('location/', csrf_exempt(views.updateLocation), name = 'updateLocation'),
    path('auxiliar/', csrf_exempt(views.auxiliar), name = 'auxiliar'),
    path('getMessages/', csrf_exempt(views.getMessages), name = 'getMessages'),
    path('building/', csrf_exempt(views.updateBuilding), name = 'updateBuilding'),


    ]





	




