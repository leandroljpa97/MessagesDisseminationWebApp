from django.db import models
from django.utils import timezone

# Create your models here.

class Buildings(models.Model):
	id = models.CharField(max_length = 255, primary_key = True)
	name = models.CharField(max_length = 255)
	lat = models.FloatField()
	longit= models.FloatField()

	def __str__(self):
		return self.id

class Users(models.Model):
	ist_id = models.CharField(max_length = 10, primary_key = True)
	name = models.CharField(max_length = 255)
	build_id = models.CharField(max_length = 255)
	range_user = models.IntegerField()
	lat = models.FloatField()
	longit = models.FloatField()

	def __str__(self):
		return self.ist_id

class LogsMovements(models.Model):
	ist_id = models.CharField(max_length = 10)
	build_id = models.CharField(max_length = 255)
	start = models.DateTimeField()
	end = models.DateTimeField(blank = True, null = True)

	def __str__(self):
		return self.ist_id

class Messages(models.Model):
	content = models.CharField(max_length = 255)
	receiver = models.CharField(max_length = 255)
	date = models.DateTimeField(default = timezone.now)
	sender = models.CharField(max_length = 255)
	build_id =  models.CharField(max_length = 255)

	def __str__(self):
		return self.content

class Bots(models.Model):
	id = models.CharField(max_length = 255, primary_key = True)
	build_id = models.CharField(max_length = 255)
	password = models.CharField(max_length = 9)

	def __str__(self):
		return self.id