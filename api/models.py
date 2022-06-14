from django.db import models

import uuid
import string
import secrets
from datetime import datetime, timedelta, timezone

# Create your models here.
class Account(models.Model):
	# Auto Fields
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	emailVerified = models.BooleanField(default=False)
	created_date = models.DateTimeField(auto_now=True)

	#Non Auto Fields
	email = models.EmailField(max_length=255, unique=True)
	password = models.CharField(max_length=255)
	handle = models.CharField(max_length=50, unique=True, blank=True)
	
	def __str__(self):
		return self.email

	class Meta:
		pass

class Token(models.Model):
	def get_expiry():
		return datetime.now(timezone.utc).astimezone() + timedelta(minutes=10)

	owner = models.OneToOneField(Account, primary_key=True, on_delete=models.CASCADE, default=None)
	expiry_date = models.DateTimeField(default=get_expiry, editable=False)

	def __str__(self):
		return self.key

	class Meta:
		abstract = True

class VerifyEmailToken(Token):
	def get_key():
		alphabet = string.ascii_letters + string.digits
		while(True):
			try:
				password = ''.join(secrets.choice(alphabet) for i in range(8))
				VerifyEmailToken.objects.all().get(key=password)
			except:
				break
		return password
	key =  models.CharField(default=get_key, max_length=255, unique=True, editable=False)
