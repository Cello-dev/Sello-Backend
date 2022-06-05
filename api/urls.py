from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'accounts', views.AccountViewSet)
urlpatterns = [
	path('auth', include('rest_framework.urls', namespace='rest_framework')),
	path('account/<str:email>', views.AccountView.as_view(), name="account"),
	path('login', views.LoginView.as_view(), name="login"),
	path('register', views.RegisterView.as_view(), name="register"),
	path('', include(router.urls))
]
