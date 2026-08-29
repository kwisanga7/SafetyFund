from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Sum

from accounts.models import User
from membership.models import MembershipApplication
from .models import ShareTransaction, Loan

from .forms import LoanRequestForm


@login_required
def request_loan(request):

    if request.method == 'POST':

        form = LoanRequestForm(request.POST,user=request.user)

        if form.is_valid():

            loan = form.save(commit=False)

            loan.member = request.user

            loan.status = 'PENDING'

            loan.save()

            return redirect('dashboard')

    else:

        form = LoanRequestForm(user=request.user)

    return render(
        request,
        'finance/request_loan.html',
        {'form': form}
    )

@login_required
def finance_dashboard(request):

    if request.user.role != 'FINANCE':
        return render(
            request,
            'finance/access_denied.html'
        )

    total_members = User.objects.filter(
        role='MEMBER'
    ).count()

    total_shares = ShareTransaction.objects.aggregate(
        total=Sum('shares')
    )['total'] or 0

    total_savings = total_shares * 5000

    pending_loans = Loan.objects.filter(
        status='PENDING'
    ).count()

    approved_loans = Loan.objects.filter(
        status='APPROVED'
    ).count()

    outstanding_loans = Loan.objects.filter(
        status='APPROVED'
    ).aggregate(
        total=Sum('requested_amount')
    )['total'] or 0

    context = {
        'total_members': total_members,
        'total_shares': total_shares,
        'total_savings': total_savings,
        'pending_loans': pending_loans,
        'approved_loans': approved_loans,
        'outstanding_loans': outstanding_loans,
    }

    return render(
        request,
        'finance/finance_dashboard.html',
        context
    )