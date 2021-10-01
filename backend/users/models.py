from django.contrib.auth.models import AbstractUser
from django.db import models

from config import settings

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    email = models.EmailField(
        'Адрес электронной почты',
        unique=True,)
    username = models.CharField(
        max_length=150,
        unique=True,
        verbose_name='Юзернейм')
    first_name = models.CharField('Имя', max_length=150)
    last_name = models.CharField('Фамилия', max_length=150)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = CustomUserManager()

    class Meta:
        ordering = ['-id']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class Follow(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="follower",
        verbose_name='Подписчик'
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="following",
        verbose_name='Автор'
    )

    class Meta:
        ordering = ['id']
        verbose_name = 'Подписка',
        verbose_name_plural = 'Подписки'
        constraints = [models.UniqueConstraint(
            fields=['user', 'author'],
            name='follow_unique'
        )]

    def __str__(self):
        return (
            f'{self.user.username} подписан '
            f'на {self.author.username}'
        )
