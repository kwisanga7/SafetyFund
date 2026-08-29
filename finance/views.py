from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from accounts.models import User
from membership.models import MembershipApplication
from .models import ShareTransaction, Loan
from django.shortcuts import get_object_or_404
from .forms import LoanRequestForm
from .models import LoanRepayment
from django.contrib.auth import get_user_model
from .models import ShareTransaction
from .forms import DepositRequestForm
from .models import DepositRequest
from datetime import datetime
from decimal import Decimal
from django.shortcuts import get_object_or_404

User = get_user_model()



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

@login_required
def pending_loans(request):

    if request.user.role != 'FINANCE':
        return render(
            request,
            'finance/access_denied.html'
        )

    loans = Loan.objects.filter(
        status='PENDING'
    )

    return render(
        request,
        'finance/pending_loans.html',
        {'loans': loans}
    )

@login_required
def approve_loan(request, loan_id):

    if request.user.role != 'FINANCE':
        return render(
            request,
            'finance/access_denied.html'
        )

    loan = get_object_or_404(
        Loan,
        id=loan_id
    )

    loan.status = 'APPROVED'

    loan.save()

    return redirect(
        'pending_loans'
    )

@login_required
def reject_loan(request, loan_id):

    if request.user.role != 'FINANCE':
        return render(
            request,
            'finance/access_denied.html'
        )

    loan = get_object_or_404(
        Loan,
        id=loan_id
    )

    loan.status = 'REJECTED'

    loan.save()

    return redirect(
        'pending_loans'
    )

@login_required
def mark_loan_paid(
    request,
    loan_id
):

    if request.user.role != 'FINANCE':

        return render(
            request,
            'finance/access_denied.html'
        )

    loan = get_object_or_404(
        Loan,
        id=loan_id
    )

    LoanRepayment.objects.create(
        loan=loan,
        amount_paid=loan.requested_amount,
        received_by=request.user
    )

    loan.status = 'PAID'

    loan.save()

    return redirect(
        'pending_loans'
    )



@login_required
def compliance_report(request):

    members = User.objects.filter(role='MEMBER')

    report = []

    for member in members:

        shares = ShareTransaction.objects.filter(
            member=member,
            month=8,
            year=2026
        )

        total_shares = sum(
            item.shares
            for item in shares
        )

        status = "Compliant" if total_shares >= 1 else "Defaulter"

        report.append({
            "member": member,
            "shares": total_shares,
            "status": status
        })

    return render(
        request,
        "finance/compliance_report.html",
        {"report": report}
    )

@login_required
def deposit_request(request):

    if request.method == 'POST':

        form = DepositRequestForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            deposit = form.save(
                commit=False
            )

            deposit.member = request.user

            deposit.save()

            return redirect(
                'dashboard'
            )

    else:

        form = DepositRequestForm()

    return render(
        request,
        'finance/deposit_request.html',
        {'form': form}
    )

@login_required
def approve_deposit(request, deposit_id):

    if request.user.role != 'FINANCE':
        return render(
            request,
            'finance/access_denied.html'
        )

    deposit = get_object_or_404(
        DepositRequest,
        id=deposit_id
    )

    if deposit.status == 'PENDING':

        shares = int(
            deposit.amount / Decimal('5000')
        )

        ShareTransaction.objects.create(
            member=deposit.member,
            shares=shares,
            amount=deposit.amount,
            month=datetime.now().month,
            year=datetime.now().year
        )

        deposit.status = 'APPROVED'
        deposit.save()

    return redirect(
        'finance_dashboard'
    )

@login_required
def reject_deposit(request, deposit_id):

    if request.user.role != 'FINANCE':
        return render(
            request,
            'finance/access_denied.html'
        )

    deposit = get_object_or_404(
        DepositRequest,
        id=deposit_id
    )

    deposit.status = 'REJECTED'
    deposit.save()

    return redirect(
        'finance_dashboard'
    )

@login_required
def pending_deposits(request):

    if request.user.role != 'FINANCE':
        return render(
            request,
            'finance/access_denied.html'
        )

    deposits = DepositRequest.objects.filter(
        status='PENDING'
    )

    return render(
        request,
        'finance/pending_deposits.html',
        {'deposits': deposits}
    )