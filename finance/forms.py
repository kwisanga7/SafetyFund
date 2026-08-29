from django import forms
from .models import Loan
from django.db.models import Sum
from .models import Loan, ShareTransaction
from .models import DepositRequest


class LoanRequestForm(forms.ModelForm):

    class Meta:
        model = Loan
        fields = ['requested_amount']

    def __init__(self, *args, **kwargs):

        self.user = kwargs.pop('user')

        super().__init__(*args, **kwargs)

    def clean_requested_amount(self):

        requested_amount = self.cleaned_data[
            'requested_amount'
        ]

        total_shares = (
            ShareTransaction.objects
            .filter(member=self.user)
            .aggregate(
                total=Sum('shares')
            )['total'] or 0
        )

        active_loans = Loan.objects.filter(
            member=self.user,
            status='APPROVED'
        )

        locked_shares = sum(
            loan.locked_shares
            for loan in active_loans
        )

        available_shares = (
            total_shares -
            locked_shares
        )

        available_loan = (
            available_shares * 5000
        )

        if requested_amount > available_loan:

            raise forms.ValidationError(
                f"You can request up to "
                f"{available_loan} RWF only."
            )

        return requested_amount




class DepositRequestForm(forms.ModelForm):

    class Meta:
        model = DepositRequest
        fields = [
            'amount',
            'payment_proof'
        ]