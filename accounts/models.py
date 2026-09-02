from django.contrib.auth.models import AbstractUser
from django.db import models
from django.forms import ModelForm

class User(AbstractUser):

    ROLE_CHOICES = (
        ('USER', 'User'),
        ('MEMBER', 'Member'),
        ('FINANCE', 'Finance Officer'),
        ('ADMINISTRATOR', 'Administrator'),
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

    address = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    bio = models.TextField(
        blank=True,
        null=True
    )

    profile_picture = models.ImageField(
        upload_to='profile_pictures/',
        blank=True,
        null=True
    )

    def __str__(self):
        return self.username






class Announcement(models.Model):

    title = models.CharField(
        max_length=200
    )

    image = models.ImageField(
        upload_to='announcements/',
        blank=True,
        null=True
    )

    description = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.title

