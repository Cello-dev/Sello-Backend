from rest_framework import serializers


from .models import Account, Product, VerifyEmailToken

# Account Serializers
class AccountSerializer(serializers.ModelSerializer): # Debug Use Only.
	class Meta:
		model = Account
		fields = '__all__'

class UpdateAccountSerializer(serializers.ModelSerializer): # Fields that are updateable.
	class Meta:
		model = Account
		fields = ('avatar_url', 'name')

class PublicAccountSerializer(serializers.ModelSerializer): # Public Data.
	class Meta:
		model = Account
		fields = ('id', 'email', 'handle', 'date_joined','email_verified', 'avatar_url', 'name')

class PrivateAccountSerializer(serializers.ModelSerializer): # Private Data.
	class Meta:
		model = Account
		fields = ('id', 'email', 'handle', 'date_joined','email_verified', 'avatar_url', 'name', 'first_name', 'last_name')

class ProductSerializer(serializers.ModelSerializer):
	class Meta:
		model = Product
		fields = '__all__'

class LoginSerializer(serializers.ModelSerializer): # Asks for the required fields for login.
	class Meta:
		model = Account
		fields = ('email', 'password')

class RegisterSerializer(serializers.ModelSerializer): # Asks for the required fields for registration.
	def create(self, validated_data): # Ensures to use to the AbstractUser.set_password() for password hashing.
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

class ForgotPasswordSerializer(serializers.ModelSerializer): # Asks for the required fields for forgot password.
	class Meta:
		model = Account
		fields = ('email',)

class ResetPasswordSerializer(serializers.Serializer): # Asks for the required fields for reseting a password.
	key = serializers.CharField(max_length=8)
	password = serializers.CharField(max_length=255)

# Token Serializers
class VerificationTokenSerializer(serializers.ModelSerializer): # Shows all the data from an Token.
	class Meta:
		model = VerifyEmailToken
		fields = '__all__'

# Misc Serializers
class TokenSerializer(serializers.Serializer): # Asks for the required fields for Email Verification.
	key = serializers.CharField(max_length=8)



