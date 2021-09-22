from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


class Profile(models.Model):
	name=models.CharField(max_length=200)
	image=models.ImageField(upload_to='Post', null=True, blank=True)
	address = models.CharField(max_length=200)
	contact = models.IntegerField()
	date=models.DateTimeField(default=datetime.now(), blank=None, null=None)