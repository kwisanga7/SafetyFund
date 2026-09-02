from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from membership.models import MembershipApplication
from .forms import LoanRequestForm
from .models import LoanRepayment
from django.contrib.auth import get_user_model
from .forms import DepositRequestForm
from datetime import datetime
from decimal import Decimal
from django.shortcuts import get_object_or_404
from accounts.models import User
from .models import ShareTransaction, Loan, DepositRequest
from .forms import LoanRepaymentForm
from .forms import MemberRepaymentForm
from decimal import Decimal
from finance.models import (ShareTransaction, Loan, DepositRequest)
from accounts.models import Announcement
from notifications.models import Notification

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

    Notification.objects.create(
    user=loan.member,
    title='Loan Approved',
    message=f'Your loan request of {loan.amount} RWF has been approved.'
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

        Notification.objects.create(
    user=deposit.member,
    title='Deposit Approved',
    message=f'Your deposit of {deposit.amount} RWF has been approved.'
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
def active_loans(request):

    if request.user.role != 'FINANCE':
        return render(
            request,
            'finance/access_denied.html'
        )

    loans = Loan.objects.filter(
        status='APPROVED'
    )

    return render(
        request,
        'finance/active_loans.html',
        {'loans': loans}
    )

@login_required
def record_repayment(request, loan_id):

    if request.user.role != 'FINANCE':
        return render(
            request,
            'finance/access_denied.html'
        )

    loan = Loan.objects.get(id=loan_id)

    if request.method == 'POST':

        form = LoanRepaymentForm(
            request.POST
        )

        if form.is_valid():

            repayment = form.save(
                commit=False
            )

            repayment.loan = loan

            repayment.save()

            loan.remaining_balance -= (
                repayment.amount_paid
            )

            if loan.remaining_balance <= 0:

                loan.remaining_balance = 0
                loan.status = 'COMPLETED'
                loan.locked_shares = 0

            loan.save()

            return redirect(
                'active_loans'
            )

    else:

        form = LoanRepaymentForm()

    return render(
        request,
        'finance/record_repayment.html',
        {
            'loan': loan,
            'form': form
        }
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

    return redirect(
        'pending_repayments'
    )



@login_required
def dashboard(request):

    total_shares = ShareTransaction.objects.filter(
        member=request.user
    ).count()

    total_deposits = DepositRequest.objects.filter(
        member=request.user,
        status='APPROVED'
    ).count()

    active_loans = Loan.objects.filter(
        member=request.user,
        status='APPROVED'
    ).count()

    pending_requests = DepositRequest.objects.filter(
        member=request.user,
        status='PENDING'
    ).count()

    context = {
        'total_shares': total_shares,
        'total_deposits': total_deposits,
        'active_loans': active_loans,
        'pending_requests': pending_requests,
    }

    return render(
        request,
        'accounts/dashboard.html',
        context
    )



def home(request):

    latest_announcements = Announcement.objects.order_by(
        '-created_at'
    )[:3]

    context = {
        'latest_announcements': latest_announcements
    }

    return render(
        request,
        'home.html',
        context
    )