from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    first_name = models.CharField(max_length=40, verbose_name='ФИО или наименование организации')
    phone = models.CharField(max_length=100)

    def __str__(self):
        return self.get_full_name()
