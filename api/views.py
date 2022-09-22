from rest_framework import generics, viewsets, status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser

from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from datetime import datetime, timezone

from api.gmail import send_email, make_verify_email, make_reset_email
from .serializers import *
from .models import Account, VerifyEmailToken, ResetPasswordToken

# Create your views here.
class AccountByHandleView(generics.RetrieveAPIView):
	queryset = Account.objects.all()
	serializer_class = PublicAccountSerializer
	permission_classes = (IsAuthenticated,)
	lookup_field = "handle"

class AccountByIDView(generics.RetrieveAPIView):
	queryset = Account.objects.all()
	serializer_class = PublicAccountSerializer
	permission_classes = (IsAuthenticated,)
	lookup_field = "id"

class AccountByTokenView(APIView):
	permission_classes = (IsAuthenticated,)
	def get(self, request):
		try:
			auth = request.headers["Authorization"]
			token = auth[6:] # Trim Auth Token
			token_record = Token.objects.get(key=token) # Search for matching token
			user = PrivateAccountSerializer(token_record.user) # Serialize associated account data.
			return Response({'msg':user.data}, status=status.HTTP_200_OK)
		except Exception as e:
			return Response({'error':str(e)}, status=status.HTTP_403_FORBIDDEN)

class UpdateAccountView(generics.UpdateAPIView):
	serializer_class = UpdateAccountSerializer
	permission_classes = (IsAuthenticated,)
	parser_classes = (MultiPartParser, FormParser)
	lookup_field = "id"

	def update(self, request, *args, **kwargs):
		return super().update(request, *args, **kwargs)
	
	def get_queryset(self):
		queryset = Account.objects.filter(id=self.request.user.id)
		return queryset

class LoginView(APIView):
	serializer_class = LoginSerializer
	def post(self, request):
		try:
			account = Account.objects.get(email__iexact=request.data["email"]) #Try to Look up the account based on email. Throws an exception
			if account.check_password(raw_password=request.data["password"]):
				auth_token, _ = Token.objects.update_or_create(user=account)
				public_account = PublicAccountSerializer(account)
				response = {'token':auth_token.key, 'data':public_account.data}
				return Response(response, status=status.HTTP_200_OK)
		except Exception as e:
			return Response({"error":str(e)}, status=status.HTTP_401_UNAUTHORIZED)
		return Response({"error":"Incorrect Email or Password"}, status=status.HTTP_401_UNAUTHORIZED)

class RegisterView(APIView):
	serializer_class = RegisterSerializer
	def post(self, request):
		account = RegisterSerializer(data=request.data)
		if account.is_valid():
			account_obj = account.create(validated_data=account.data)
			code = VerifyEmailToken(account_obj.id)
			code.save()
			success = send_email(make_verify_email(account_obj.email, code.key))
			if success:
				public_account = PublicAccountSerializer(account_obj)
				response = {"message":"Verification Email sent to {email}".format(email=account_obj.email), "data":public_account.data}
			else:
				response = {"error":"Verification Email Failed", "data":public_account.data}
			return Response(response, status=status.HTTP_201_CREATED)
		return Response(account.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyEmailView(APIView):
	serializer_class = TokenSerializer
	def post(self, request):
		try:
			token = VerifyEmailToken.objects.get(key=request.data["key"])
			now = (datetime.now(timezone.utc).astimezone())
			if now <= token.expiry_date:
				if not token.owner.emailVerified:
					token.owner.emailVerified = True
					token.owner.save(update_fields=['emailVerified'])
					email = token.owner.email
					token.delete()
					return Response({"message":email + " has been verified."}, status=status.HTTP_200_OK)
				return Response({"message":email + " already verified."}, status=status.HTTP_409_CONFLICT)
			else:
				token.delete()
				return Response({"message":"Token is expired"}, status=status.HTTP_401_UNAUTHORIZED)
		except Exception as e:
			return Response({"error":str(e)}, status=status.HTTP_404_NOT_FOUND)

class EmailResendView(APIView):
	serializer_class = ForgotPasswordSerializer
	def post(self, request):
		try:
			account = Account.objects.get(email__iexact=request.data["email"])
			if not account.emailVerified:
				code = VerifyEmailToken(account.id)
				code.save()
				send_email(make_verify_email(account.email, code.key))
				return Response({"message":"A verification email has been sent to {email}.".format(email=account.email)}, status=status.HTTP_200_OK)
			return Response({"message":"Email Already Verified"}, status=status.HTTP_200_OK)
		except Exception as e:
			return Response({"error":str(e)}, status=status.HTTP_404_NOT_FOUND)

class ForgotPasswordView(APIView):
	serializer_class = ForgotPasswordSerializer
	def post(self, request):
		try:
			account = Account.objects.get(email__iexact=request.data["email"])
			code = ResetPasswordToken(account.id)
			code.save()
			send_email(make_reset_email(account.email, code.key))
			return Response({"message":"A recovery email has been sent to {email}.".format(email=account.email)}, status=status.HTTP_200_OK)
		except Exception as e:
			return Response({"error":str(e)}, status=status.HTTP_404_NOT_FOUND)

class ValidateTokenView(APIView):
	serializer_class = TokenSerializer
	def post(self, request):
		token_request = TokenSerializer(data=request.data)
		if token_request.is_valid():
			try:
				token = ResetPasswordToken.objects.get(key=token_request.data["key"])
				now = (datetime.now(timezone.utc).astimezone())
				if now <= token.expiry_date:
					token.isValidated = True
					token.save(update_fields=['isValidated'])
					return Response({"message":"Token is valid"}, status=status.HTTP_200_OK)
			except Exception as e:
				return Response({"error":str(e)}, status=status.HTTP_404_NOT_FOUND)

class ResetPasswordView(APIView):
	serializer_class = ResetPasswordSerializer
	def post(self, request):
		print(request.data)
		request_serializer = ResetPasswordSerializer(data=request.data)
		if(request_serializer.is_valid()):
			try:
				token = ResetPasswordToken.objects.get(key=request_serializer.data["key"])
				if token.isValidated:
					now = (datetime.now(timezone.utc).astimezone())
					if now <= token.expiry_date:
						token.owner.set_password(request_serializer.data["password"])
						token.owner.save(update_fields=['password'])
						token.delete()
						return Response({"message":"Password has been reset"}, status=status.HTTP_200_OK)
					else:
						token.delete()
						return Response({"message":"Token is expired"}, status=status.HTTP_401_UNAUTHORIZED)
			except Exception as e:
				return Response({"error":str(e)}, status=status.HTTP_404_NOT_FOUND)
		return Response({"error":"Invalid Request"}, status=status.HTTP_400_BAD_REQUEST)