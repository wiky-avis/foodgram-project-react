from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from backend.config import settings

User = get_user_model()


class UserRole(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(
        'Уровень доступа',
        max_length=20,
        choices=settings.ROLES,
        default=settings.USER
    )

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

    @property
    def is_guest(self):
        return self.role == settings.GUEST

    @property
    def is_user(self):
        return self.role == settings.USER

    @property
    def is_admin(self):
        return self.role == settings.ADMINISTRATOR


@receiver(post_save, sender=User)
def create_user_role(sender, instance, created, **kwargs):
    if created:
        UserRole.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_role(sender, instance, **kwargs):
    instance.profile.save()
