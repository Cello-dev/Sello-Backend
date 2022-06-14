from django.contrib import admin
from .models import Account, VerifyEmailToken

# Register your models here.
admin.site.register(Account)
admin.site.register(VerifyEmailToken)