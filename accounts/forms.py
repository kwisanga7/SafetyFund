from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class RegisterForm(UserCreationForm):

    email = forms.EmailField()

    class Meta:
        model = User

        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2'
        )

    def clean_email(self):

        email = self.cleaned_data['email']

        if User.objects.filter(email=email).exists():

            raise forms.ValidationError(
                'This email is already registered.'
            )

        return email

    def clean_first_name(self):

        first_name = self.cleaned_data['first_name']

        if len(first_name) < 2:

            raise forms.ValidationError(
                'First name is too short.'
            )

        return first_name

    def clean_last_name(self):

        last_name = self.cleaned_data['last_name']

        if len(last_name) < 2:

            raise forms.ValidationError(
                'Last name is too short.'
            )

        return last_name




class ProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = User

        fields = [
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'address',
            'bio',
            'profile_picture',
        ]