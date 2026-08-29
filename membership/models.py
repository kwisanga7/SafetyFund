from django.utils import timezone
from datetime import datetime
from django.db import models
from django.conf import settings


class MembershipApplication(models.Model):

    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    national_id = models.CharField(max_length=20)

    phone_number = models.CharField(max_length=20)

    address = models.CharField(max_length=255)

    occupation = models.CharField(max_length=100)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDING'
    )

    applied_at = models.DateTimeField(auto_now_add=True)

    reviewed_at = models.DateTimeField(
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.user.username} - {self.status}"

    member_number = models.CharField(
    max_length=20,
    unique=True,
    null=True,
    blank=True
    )

    approved_date = models.DateTimeField(
    null=True,
    blank=True
    )

    status = models.CharField(
    max_length=20,
    choices=STATUS_CHOICES,
    default='PENDING'
    )

    member_number = models.CharField(
    max_length=20,
    unique=True,
    null=True,
    blank=True
    )

    approved_date = models.DateTimeField(
    null=True,
    blank=True
    )

    applied_at = models.DateTimeField(auto_now_add=True)

    reviewed_at = models.DateTimeField(
    null=True,
    blank=True
    )

    def save(self, *args, **kwargs):

     if self.status == 'APPROVED':

        if not self.member_number:

            year = datetime.now().year

            last_member = MembershipApplication.objects.filter(
                member_number__isnull=False
            ).count()

            next_number = last_member + 1

            self.member_number = (
                f"SF{year}{next_number:03d}"
            )

        if not self.approved_date:
            self.approved_date = timezone.now()

        self.user.role = 'MEMBER'
        self.user.save()

     super().save(*args, **kwargs)