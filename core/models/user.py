from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    email = models.EmailField("e-mail", unique=True)
    first_name = models.CharField("nome", max_length=150, blank=True)
    last_name = models.CharField("sobrenome", max_length=150, blank=True)

    class Meta:
        verbose_name = "usuário"
        verbose_name_plural = "usuários"

    def __str__(self):
        return self.email or self.username
