from django.db import models
import uuid

# Create your models here.
class Account(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	email = models.EmailField(max_length=255, unique=True)
	password = models.CharField(max_length=255)
	created_on = models.DateTimeField(auto_now=True)
	
	def __str__(self):
		return self.email
		
class Login(models.Model):
	email = models.EmailField(max_length=255)
	password = models.CharField(max_length=255)
	
	def __str__(self):
		return self.email + " : " + self.password
