from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):
    def _create_user(self, email, username, password, **extra_fields):
        if not email:
            raise ValueError('Заполните поле email')
        if not username:
            raise ValueError('Заполните поле username')
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            username=username,
            **extra_fields,)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, username, password, **extra_fields):
        user = self._create_user(
            email,
            username,
            password,
            **extra_fields)
        return user

    def create_superuser(self, email, username, password, **extra_fields):
        user = self._create_user(
            email,
            username,
            password,
            is_staff=True,
            is_superuser=True,
            **extra_fields)
        return user
