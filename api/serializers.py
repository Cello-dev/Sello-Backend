from rest_framework import serializers

from .models import Account, VerifyEmailToken

# Account Serializers
class AccountSerializer(serializers.ModelSerializer): # Shows all the data from an account.

	class Meta:
		model = Account
		fields = '__all__'

class PublicAccountSerializer(serializers.ModelSerializer): # Only shows the publicly available data from an Account.
	class Meta:
		model = Account
		fields = ('id', 'handle', 'email', 'emailVerified')

class AccountRegisterSerializer(serializers.ModelSerializer): # Asks for the required fields for registrations.
	def create(self, validated_data):
		account = Account.objects.create(
			email=validated_data["email"],
			handle=validated_data["handle"]
		)
		account.set_password(validated_data['password'])
		account.save()
		return account
	class Meta:
		model = Account
		fields = ('email', 'password', 'handle')

class AccountLoginSerializer(serializers.ModelSerializer): # Asks for the required fields for registrations.
	class Meta:
		model = Account
		fields = ('email', 'password')

class ForgotPasswordSerializer(serializers.ModelSerializer): # Asks for the required fields for forgot password.
	class Meta:
		model = Account
		fields = ('email',)

# Token Serializers
class VerificationTokenSerializer(serializers.ModelSerializer): # Shows all the data from an Token.
	class Meta:
		model = VerifyEmailToken
		fields = '__all__'

# Misc Serializers
class TokenSerializer(serializers.Serializer): # Asks for the required fields for Email Verification.
	key = serializers.CharField(max_length=8)

class ResetPasswordSerializer(serializers.Serializer): # Asks for the required fields for reseting a password.
	key = serializers.CharField(max_length=8)
	password = serializers.CharField(max_length=255)

