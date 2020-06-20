from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    class Meta:
        db_table = "api_user"
        verbose_name = "user"
        verbose_name_plural = "users"
        ordering = ["id"]

    def __str__(self):
        return self.get_full_name()

    bio = models.CharField(max_length=160)
