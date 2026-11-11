from datetime import datetime
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from activitylogs.models import ActivityLog
from notifications.services import notify_roles, notify_user

from .forms import (
    DepositRequestForm,
    LoanRequestForm,
    MemberRepaymentForm,
)
from .models import DepositRequest, Loan, LoanRepayment, ShareTransaction

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

            ActivityLog.objects.create(
    user=request.user,
    action='Submitted loan request'
)

            notify_roles(
                ['FINANCE'],
                title='New loan request',
                message=f'{request.user.username} submitted a loan request.',
                link=reverse('pending_loans'),
                exclude=request.user,
            )

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

    current_month = datetime.now().month
    current_year = datetime.now().year

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

    active_loans = Loan.objects.filter(
        status='APPROVED'
    ).count()

    outstanding_loans = Loan.objects.filter(
        status='APPROVED'
    ).aggregate(
        total=Sum('requested_amount')
    )['total'] or 0

    pending_deposits = DepositRequest.objects.filter(
        status='PENDING'
    ).count()

    approved_deposits = DepositRequest.objects.filter(
        status='APPROVED'
    ).count()

    monthly_deposits = DepositRequest.objects.filter(
        status='APPROVED',
        submitted_at__month=current_month,
        submitted_at__year=current_year
    ).aggregate(
        total=Sum('amount')
    )['total'] or 0

    context = {
        'total_members': total_members,
        'total_shares': total_shares,
        'total_savings': total_savings,
        'pending_loans': pending_loans,
        'active_loans': active_loans,
        'outstanding_loans': outstanding_loans,
        'pending_deposits': pending_deposits,
        'approved_deposits': approved_deposits,
        'monthly_deposits': monthly_deposits,
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

    notify_user(
        loan.member,
        title='Loan approved',
        message=f'Your loan request of {loan.requested_amount} RWF has been approved.',
        link=reverse('my_loans'),
    )

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

    notify_user(
        loan.member,
        title='Loan request update',
        message=f'Your loan request of {loan.requested_amount} RWF was not approved.',
        link=reverse('my_loans'),
    )

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

    final_payment = loan.remaining_balance or loan.requested_amount

    LoanRepayment.objects.create(
        loan=loan,
        amount_paid=final_payment,
        status='APPROVED',
    )

    loan.status = 'PAID'
    loan.remaining_balance = Decimal('0.00')

    loan.save()

    notify_user(
        loan.member,
        title='Loan marked as paid',
        message='Your loan has been marked as paid.',
        link=reverse('my_loans'),
    )

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

            ActivityLog.objects.create(
             user=request.user,
             action='Submitted deposit request'
            )

            notify_roles(
                ['FINANCE'],
                title='New deposit request',
                message=f'{request.user.username} submitted a deposit of {deposit.amount} RWF.',
                link=reverse('pending_deposits'),
                exclude=request.user,
            )

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

        notify_user(
            deposit.member,
            title='Deposit approved',
            message=f'Your deposit of {deposit.amount} RWF has been approved.',
            link=reverse('dashboard'),
        )

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

    notify_user(
        deposit.member,
        title='Deposit request update',
        message=f'Your deposit of {deposit.amount} RWF was not approved.',
        link=reverse('dashboard'),
    )

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


@login_required
def deposit_history(request):
    if request.user.role not in ['FINANCE', 'ADMINISTRATOR', 'DEVELOPER']:
        return render(request, 'finance/access_denied.html')

    deposits = DepositRequest.objects.select_related('member').order_by(
        '-submitted_at'
    )
    status = request.GET.get('status')
    valid_statuses = {value for value, _label in DepositRequest.STATUS_CHOICES}

    if status in valid_statuses:
        deposits = deposits.filter(status=status)

    period = request.GET.get('period')
    if period == 'month':
        deposits = deposits.filter(
            submitted_at__month=datetime.now().month,
            submitted_at__year=datetime.now().year,
        )

    return render(
        request,
        'finance/deposit_history.html',
        {'deposits': deposits, 'status': status, 'period': period},
    )


@login_required
def loan_records(request):
    if request.user.role not in ['FINANCE', 'ADMINISTRATOR', 'DEVELOPER']:
        return render(request, 'finance/access_denied.html')

    loans = Loan.objects.select_related('member').order_by('-requested_at')
    status = request.GET.get('status')
    valid_statuses = {value for value, _label in Loan.STATUS_CHOICES}

    if status in valid_statuses:
        loans = loans.filter(status=status)

    return render(
        request,
        'finance/loan_records.html',
        {'loans': loans, 'status': status},
    )

@login_required
def make_repayment(request, loan_id):

    loan = Loan.objects.get(
        id=loan_id,
        member=request.user
    )

    if request.method == 'POST':

        form = MemberRepaymentForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            repayment = form.save(
                commit=False
            )

            repayment.loan = loan

            repayment.save()

            notify_roles(
                ['FINANCE'],
                title='New loan repayment request',
                message=f'{request.user.username} submitted a repayment of {repayment.amount_paid} RWF.',
                link=reverse('pending_repayments'),
                exclude=request.user,
            )

            return redirect(
                'dashboard'
            )

    else:

        form = MemberRepaymentForm(
            initial={
                'amount_paid':
                loan.remaining_balance
            }
        )

    return render(
        request,
        'finance/make_repayment.html',
        {
            'loan': loan,
            'form': form
        }
    )

@login_required
def pending_repayments(request):

    if request.user.role != 'FINANCE':
        return render(
            request,
            'finance/access_denied.html'
        )

    repayments = LoanRepayment.objects.filter(
        status='PENDING'
    )

    return render(
        request,
        'finance/pending_repayments.html',
        {
            'repayments': repayments
        }
    )

@login_required
def approve_repayment(request, repayment_id):

    if request.user.role != 'FINANCE':
        return render(
            request,
            'finance/access_denied.html'
        )

    repayment = LoanRepayment.objects.get(
        id=repayment_id
    )

    if repayment.status == 'PENDING':

        loan = repayment.loan

        loan.remaining_balance -= repayment.amount_paid

        if loan.remaining_balance <= Decimal('0.00'):

            loan.remaining_balance = Decimal('0.00')
            loan.status = 'COMPLETED'
            loan.locked_shares = 0

        loan.save()

        repayment.status = 'APPROVED'
        repayment.save()

        notify_user(
            loan.member,
            title='Repayment approved',
            message=f'Your repayment of {repayment.amount_paid} RWF has been approved.',
            link=reverse('my_loans'),
        )

    return redirect(
        'pending_repayments'
    )

@login_required
def reject_repayment(request, repayment_id):

    if request.user.role != 'FINANCE':
        return render(
            request,
            'finance/access_denied.html'
        )

    repayment = LoanRepayment.objects.get(
        id=repayment_id
    )

    repayment.status = 'REJECTED'
    repayment.save()

    notify_user(
        repayment.loan.member,
        title='Repayment request update',
        message=f'Your repayment of {repayment.amount_paid} RWF was not approved.',
        link=reverse('my_loans'),
    )

    return redirect(
        'pending_repayments'
    )

@login_required
def my_loans(request):

    loans = Loan.objects.filter(
        member=request.user
    )

    return render(
        request,
        'finance/active_loans.html',
        {
            'loans': loans
        }
    )
