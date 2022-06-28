from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import AccountManager

import uuid
import string
import secrets
from datetime import datetime, timedelta, timezone

# Create your models here.
class Account(AbstractUser):
	username = None
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	email = models.EmailField(unique=True)
	handle = models.CharField(max_length=50, blank=True)
	emailVerified = models.BooleanField(default=False)

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = []

	objects = AccountManager()

	def __str__(self):
		return self.email

	class Meta:
		pass

class MyAbstractToken(models.Model):
	def generate_expiry(time_delta):
		return datetime.now(timezone.utc).astimezone() + time_delta
	def generate_token(model, length):
		alphabet = string.ascii_letters + string.digits
		while(True):
			try:
				password = ''.join(secrets.choice(alphabet) for i in range(length))
				model.objects.all().get(key=password)
			except:
				break
		return password

	owner = models.OneToOneField(Account, primary_key=True, on_delete=models.CASCADE, default=None)

	class Meta:
		abstract = True

class VerifyEmailToken(MyAbstractToken):
	def get_key():
		return MyAbstractToken.generate_token(VerifyEmailToken, 8)
	def get_expiry():
		return MyAbstractToken.generate_expiry(timedelta(minutes=10))


	key =  models.CharField(default=get_key, max_length=255, unique=True, editable=False)
	expiry_date = models.DateTimeField(default=get_expiry, editable=False)

	def __str__(self):
		return self.key

class ResetPasswordToken(MyAbstractToken):
	def get_key():
		return MyAbstractToken.generate_token(ResetPasswordToken, 8)
	def get_expiry():
		return MyAbstractToken.generate_expiry(timedelta(minutes=10))

	key =  models.CharField(default=get_key, max_length=255, unique=True, editable=False)
	expiry_date = models.DateTimeField(default=get_expiry, editable=False)
	isValidated = models.BooleanField(default=False)

	def __str__(self):
		return self.key

