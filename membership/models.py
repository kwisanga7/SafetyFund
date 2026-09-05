from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import datetime

import qrcode

from io import BytesIO
from django.core.files import File


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

    national_id = models.CharField(
        max_length=20
    )

    phone_number = models.CharField(
        max_length=20
    )

    address = models.CharField(
        max_length=255
    )

    occupation = models.CharField(
        max_length=100
    )

    payment_proof = models.FileField(
        upload_to='membership_proofs/',
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

    applied_at = models.DateTimeField(
        auto_now_add=True
    )

    reviewed_at = models.DateTimeField(
        null=True,
        blank=True
    )

    approved_date = models.DateTimeField(
        null=True,
        blank=True
    )

    qr_code = models.ImageField(
        upload_to='member_qr_codes/',
        blank=True,
        null=True
    )

    def save(self, *args, **kwargs):

        if self.status == 'APPROVED':

            # Generate member number
            if not self.member_number:

                year = datetime.now().year

                last_member = MembershipApplication.objects.filter(
                    member_number__isnull=False
                ).count()

                next_number = last_member + 1

                self.member_number = (
                    f"SF{year}{next_number:03d}"
                )

            # Set approval date
            if not self.approved_date:
                self.approved_date = timezone.now()

            # Update user role
            self.user.role = 'MEMBER'
            self.user.save()

            # Generate QR Code
            if not self.qr_code:

                qr_data = (
                    f"http://127.0.0.1:8000/"
                    f"verify-member/{self.member_number}/"
                )

                qr_image = qrcode.make(qr_data)

                buffer = BytesIO()

                qr_image.save(
                    buffer,
                    format='PNG'
                )

                filename = (
                    f"{self.member_number}.png"
                )

                self.qr_code.save(
                    filename,
                    File(buffer),
                    save=False
                )

        super().save(*args, **kwargs)

    def __str__(self):

        return (
            f"{self.user.username} - "
            f"{self.status}"
        )