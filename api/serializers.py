from rest_framework import serializers
from .models import Account
import argon2
from argon2 import PasswordHasher

class AccountSerializer(serializers.ModelSerializer):
	def create(self, data):
		ph = PasswordHasher()
		password = data["password"]
		hash = ph.hash(password)
		data["password"] = hash
		return super(AccountSerializer, self).create(data)

	class Meta:
		model = Account
		fields = '__all__'
		
class LoggedInAccountSerializer(serializers.ModelSerializer):
	class Meta:
		model = Account
		fields = ('id', 'email', 'created_on', 'handle')

class AccountLoginSerializer(serializers.ModelSerializer):
	class Meta:
		model = Account
		fields = ('email', 'password')