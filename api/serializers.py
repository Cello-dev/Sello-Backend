from rest_framework import serializers
from .models import Account, Login
import argon2
from argon2 import PasswordHasher

class AccountSerializer(serializers.ModelSerializer):
	class Meta:
		model = Account
		fields = '__all__'
		
class LoggedInAccountSerializer(serializers.ModelSerializer):
	class Meta:
		model = Account
		fields = ('id', 'email', 'created_on')
		
class LoginSerializer(serializers.ModelSerializer):
	class Meta:
		model = Login
		fields = '__all__'
	
class RegisterSerializer(serializers.ModelSerializer):
	def create(self, data):
		ph = PasswordHasher()
		password = data["password"]
		hash = ph.hash(password)
		data["password"] = hash
		return super(RegisterSerializer, self).create(data)
		
	class Meta:
		model = Account
		fields = '__all__'
