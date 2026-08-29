from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm
from finance.models import ShareTransaction
from membership.models import MembershipApplication
from django.db import models
from finance.models import Loan


def register(request):

    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            return redirect('home')

    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})


def login_user(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
         print("LOGIN SUCCESS:", user.username, user.role)
         login(request, user)
         return redirect('home')
        else:
         print("LOGIN FAILED")

    return render(request, 'accounts/login.html')
    


def logout_user(request):
    logout(request)
    return redirect('home')




@login_required
def dashboard(request):

    active_loans = Loan.objects.filter(
    member=request.user,
    status='APPROVED'
     )

    membership = MembershipApplication.objects.filter(
        user=request.user
    ).first()

    total_shares = ShareTransaction.objects.filter(
        member=request.user
    ).aggregate(
        total=models.Sum('shares')
    )['total'] or 0

    savings_value = total_shares * 5000

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
    

    context = {
        'membership': membership,
        'total_shares': total_shares,
        'locked_shares': locked_shares,
        'available_shares': available_shares,
        'savings_value': savings_value,
        'available_loan': available_loan,
    }

    return render(
        request,
        'accounts/dashboard.html',
        context
    )