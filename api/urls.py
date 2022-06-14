from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register('accounts', views.AccountViewSet, basename='accounts')
router.register('tokens', views.TokenViewSet, basename='tokens')

r = routers.SimpleRouter()

urlpatterns = [
	path('login', views.LoginView.as_view(), name="login"),
	path('register', views.RegisterView.as_view(), name="register"),
	path('account/<str:email>', views.AccountView.as_view(), name="account"),
	path('forgotpassword', views.ForgotPasswordView.as_view(), name="forgotpassword"),
	path('resetpassword', views.ResetPasswordView.as_view(), name="resetpassword"),
	path('verifyemail', views.VerifyEmailView.as_view(), name="verifyemail"),
	path('resendverifyemail', views.EmailResendView.as_view(), name="resendverifyemail"),
	path('auth', include('rest_framework.urls', namespace='rest_framework')),
	path('', include(router.urls))
]
