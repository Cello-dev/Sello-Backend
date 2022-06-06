from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()

urlpatterns = [
	path('login', views.LoginView.as_view(), name="login"),
	path('register', views.RegisterView.as_view(), name="register"),
	path('account/<str:email>', views.AccountView.as_view(), name="account"),
	path('auth', include('rest_framework.urls', namespace='rest_framework')),
	path('', include(router.urls))
]
