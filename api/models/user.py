from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    def __str__(self):
        return self.get_full_name()

    bio = models.CharField(max_length=160)