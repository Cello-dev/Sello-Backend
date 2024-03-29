from django.contrib.auth.base_user import BaseUserManager

class AccountManager(BaseUserManager):
    def create_user(self, email, password):
        email = self.normalize_email(email)
        user = self.model(email=email)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password):
        user = self.create_user(
            email,
            password,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user
