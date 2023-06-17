from django.db import models
from django.contrib.auth.models import AbstractUser

ROLE_CHOICES = (
        ('client', 'Клиент'),
        ('developer', 'Разработчик'),
        ('admin', 'Администратор')
    )


class User(AbstractUser):
    phone = models.CharField(max_length=100)
    role = models.CharField(max_length=100, choices=ROLE_CHOICES)
    organization = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(verbose_name="email address", blank=True)

    def __str__(self):
        return self.get_full_name()




