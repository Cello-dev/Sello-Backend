from django.contrib import admin

from api.serializers import ResetPasswordSerializer
from .models import Account, ResetPasswordToken, VerifyEmailToken, ResetPasswordToken

# Register your models here.
admin.site.register(Account)
admin.site.register(VerifyEmailToken)
admin.site.register(ResetPasswordToken)