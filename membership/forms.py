from django import forms
from .models import MembershipApplication


class MembershipApplicationForm(forms.ModelForm):

    class Meta:
        model = MembershipApplication

        fields = [
            'national_id',
            'phone_number',
            'address',
            'occupation',
            'payment_proof',
        ]