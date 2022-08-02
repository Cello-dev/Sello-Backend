from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers

from . import views

router = routers.DefaultRouter()

urlpatterns = [
	path('me', views.AccountByTokenView.as_view(), name='me'),
	path('login', views.LoginView.as_view(), name="login"),
	path('register', views.RegisterView.as_view(), name="register"),
	path('verifyemail', views.VerifyEmailView.as_view(), name="verifyemail"),
	path('resendverifyemail', views.EmailResendView.as_view(), name="resendverifyemail"),
	path('forgotpassword', views.ForgotPasswordView.as_view(), name="forgotpassword"),
	path('validatetoken', views.ValidateTokenView.as_view(), name="validatetoken"),
	path('resetpassword', views.ResetPasswordView.as_view(), name="resetpassword"),
	path('account/id/<uuid:id>', views.AccountByIDView.as_view(), name="account_by_id"),
	path('account/id/<uuid:id>/change', views.UpdateAccountView.as_view(), name="account_by_id"),
	path('account/<str:handle>', views.AccountByHandleView.as_view(), name="account_by_handle"),
	path('auth', include('rest_framework.urls', namespace='rest_framework')),
	path('', include(router.urls))
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)