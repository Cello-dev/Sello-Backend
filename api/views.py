from urllib import response
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.core import serializers
from rest_framework import permissions, generics, viewsets, status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import AccountSerializer, AccountLoginSerializer, LoggedInAccountSerializer
from .models import Account

import argon2
from argon2 import PasswordHasher

# Create your views here.
	
class AccountView(generics.RetrieveUpdateDestroyAPIView):
	serializer_class = AccountSerializer
	permission_classes = (IsAuthenticated,)
	lookup_field = "email"
	
	def get_queryset(self):
		queryset = Account.objects.all()
		return queryset
		
class LoginView(APIView):
	serializer_class = AccountLoginSerializer
	def post(self, request):
		try:
			account = Account.objects.get(email__iexact=request.data["email"]) #Try to Look up the account based on email. Throws an exception
			ph = PasswordHasher()
			ph.verify(account.password, request.data['password']) # Try to verify password. Throws an exception.
			response = LoggedInAccountSerializer(account)
			return Response(response.data, status=status.HTTP_200_OK)
		except:
			return Response({"error":"Incorrect Email or Password"}, status=status.HTTP_401_UNAUTHORIZED)

class RegisterView(APIView):
	serializer_class = AccountLoginSerializer
	def post(self, request):
		account = AccountSerializer(data=request.data)
		if account.is_valid():
			account_obj = account.save()
			response = LoggedInAccountSerializer(account_obj)
			return Response(response.data, status=status.HTTP_201_CREATED)
		return Response(account.errors, status=status.HTTP_400_BAD_REQUEST)
		
			
		
	
