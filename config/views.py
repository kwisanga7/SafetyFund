from django.shortcuts import render

from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    return render(request, 'accounts/dashboard.html')


def home(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')


def contact(request):
    return render(request, 'contact.html')