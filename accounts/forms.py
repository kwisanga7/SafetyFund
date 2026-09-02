from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User



class RegisterForm(UserCreationForm):

    email = forms.EmailField()

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'phone_number',
            'password1',
            'password2'
        ]




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