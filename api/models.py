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
	email_verified = models.BooleanField(default=False)

	avatar_url = models.ImageField(upload_to="images/profiles/", blank=True, null=True)
	name = models.CharField(max_length=100, blank=True)
	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = []

	objects = AccountManager()

	def __str__(self):
		return str(self.id) + " : " + str(self.email)


class Product(models.Model):
	owner = models.ForeignKey(Account, on_delete=models.CASCADE)
	name = models.CharField(max_length=150)
	description = models.TextField(max_length=300)
	tag_list = models.TextField(blank=True, default='[]')
	created_date = models.DateField(auto_now=True, editable=False)
	last_modified = models.DateField(auto_now=True)

	def __str__(self):
		return str(self.name)

class MyAbstractToken(models.Model):
	def generate_expiry(time_delta):
		return datetime.now(timezone.utc).astimezone() + time_delta
	def generate_token(model, length):
		alphabet = string.digits
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
		return MyAbstractToken.generate_token(VerifyEmailToken, 6)
	def get_expiry():
		return MyAbstractToken.generate_expiry(timedelta(minutes=10))


	key =  models.CharField(default=get_key, max_length=255, unique=True, editable=False)
	expiry_date = models.DateTimeField(default=get_expiry, editable=False)

	def __str__(self):
		return self.key

class ResetPasswordToken(MyAbstractToken):
	def get_key():
		return MyAbstractToken.generate_token(ResetPasswordToken, 6)
	def get_expiry():
		return MyAbstractToken.generate_expiry(timedelta(minutes=10))

	key =  models.CharField(default=get_key, max_length=255, unique=True, editable=False)
	expiry_date = models.DateTimeField(default=get_expiry, editable=False)
	is_validated = models.BooleanField(default=False)

	def __str__(self):
		return self.key