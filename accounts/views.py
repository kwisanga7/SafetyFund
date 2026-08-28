from django.shortcuts import render, redirect
from .forms import RegisterForm

def register(request):

    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            print("USER CREATED:", user.username)
            return redirect('home')

        else:
            print("FORM ERRORS:", form.errors)

    else:
        form = RegisterForm()

    return render(
        request,
        'accounts/register.html',
        {'form': form}
    )