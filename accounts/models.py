from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    ROLE_CHOICES = (
        ('USER', 'User'),
        ('MEMBER', 'Member'),
        ('FINANCE', 'Finance Officer'),
        ('ADMIN', 'Administrator'),
        ('DEVELOPER', 'Developer'),
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='USER'
    )

    phone_number = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.username