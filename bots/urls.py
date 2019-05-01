from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

app_name = 'bots'

urlpatterns = [
	path('', csrf_exempt(views.sendMessages), name = 'send_messages'),

]