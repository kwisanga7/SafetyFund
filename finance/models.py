from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal


class ShareTransaction(models.Model):

    SHARE_PRICE = 5000

    member = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    shares = models.PositiveIntegerField()

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        editable=False
    )

    month = models.CharField(max_length=20)

    year = models.IntegerField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def save(self, *args, **kwargs):
        self.amount = self.shares * self.SHARE_PRICE
        super().save(*args, **kwargs)

    def __str__(self):
        return (
            f"{self.member.username} - "
            f"{self.shares} shares"
        )

class Loan(models.Model):

    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('PAID', 'Paid'),
        ('REJECTED', 'Rejected'),
    )

    member = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    requested_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    fee_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    disbursed_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDING'
    )

    requested_at = models.DateTimeField(
        auto_now_add=True
    )

    due_date = models.DateField(
        null=True,
        blank=True
    )

    paid_at = models.DateTimeField(
        null=True,
        blank=True
    )

    def __str__(self):
        return (
            f"{self.member.username} - "
            f"{self.requested_amount}"
        )

    locked_shares = models.PositiveIntegerField(
    default=0
    )

    def save(self, *args, **kwargs):

     if self.status == 'APPROVED':

        # Calculate 3% fee
        self.fee_amount = ( self.requested_amount * Decimal('0.03'))

        # Amount member receives
        self.disbursed_amount = (
            self.requested_amount -
            self.fee_amount
        )

        # Shares locked
        self.locked_shares = int(
            self.requested_amount / 5000
        )

        # Due date after 30 days
        if not self.due_date:
            self.due_date = (
                timezone.now().date() +
                timedelta(days=30)
            )

     super().save(*args, **kwargs)