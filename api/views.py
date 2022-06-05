from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.core import serializers
from rest_framework import permissions, generics, viewsets, status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import AccountSerializer, LoginSerializer,LoggedInAccountSerializer,  RegisterSerializer
from .models import Account

import argon2
from argon2 import PasswordHasher

# Create your views here.

class AccountViewSet(viewsets.ModelViewSet):
	queryset = Account.objects.all().order_by('email')
	serializer_class = AccountSerializer
	permission_classes = (IsAuthenticated,)
	
class AccountView(generics.RetrieveUpdateDestroyAPIView):
	serializer_class = AccountSerializer
	permission_classes = (IsAuthenticated,)
	lookup_field = "email"
	
	def get_queryset(self):
		queryset = Account.objects.all()
		return queryset
		
		
class LoginView(APIView):
	serializer_class = LoginSerializer
	def post(self, request):
		login = LoginSerializer(data=request.data)
		if login.is_valid():
			login.save()
			try:
				account = Account.objects.get(email__iexact=login.data["email"])
				ph = PasswordHasher()
				ph.verify(account.password, login.data['password'])
				serializer = LoggedInAccountSerializer(account)
				return Response(serializer.data, status=status.HTTP_200_OK)
			except:
				return Response({"error":"Incorrect Email or Password"}, status=status.HTTP_401_UNAUTHORIZED)		
		return Response(login.errors, status=status.HTTP_400_BAD_REQUEST)
		
class RegisterView(APIView):
	serializer_class = LoginSerializer
	def post(self, request):
		login = LoginSerializer(data=request.data)
		if login.is_valid():
			account = RegisterSerializer(data=login.data)
			if account.is_valid():
				account_obj = account.save()
				response = LoggedInAccountSerializer(account_obj)
				return Response(response.data, status=status.HTTP_201_CREATED)
			else:
				return Response(account.errors, status=status.HTTP_409_CONFLICT)
		else:
			return Response(login.errors, status=status.HTTP_400_BAD_REQUEST)
	
		
			
		
	
