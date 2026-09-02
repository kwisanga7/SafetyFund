from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm
from finance.models import ShareTransaction
from membership.models import MembershipApplication
from django.db import models
from finance.models import Loan
from finance.models import DepositRequest
from finance.models import ShareTransaction, Loan
from finance.models import DepositRequest, Loan
from .models import User
from django.shortcuts import get_object_or_404
from .models import Announcement
from django.forms import ModelForm
from accounts.models import Announcement
from .forms import ProfileUpdateForm
from django.conf import settings
from membership.models import MembershipApplication
from finance.models import DepositRequest, Loan
from notifications.models import Notification



from finance.models import (
    ShareTransaction,
    DepositRequest,
    Loan,
    LoanRepayment
)

def register(request):

    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()

            admins = User.objects.filter(
               role='ADMINISTRATOR'
              )

            for admin in admins:

             Notification.objects.create(
                user=admin,
                title='New User Registration',
                message=f'{user.username} has registered.'
            )
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

            login(request, user)

            print("LOGIN SUCCESS:",user.username,user.role)

            if user.role == 'ADMINISTRATOR':
                return redirect('admin_dashboard')

            elif user.role == 'FINANCE':
                return redirect('finance_dashboard')
            elif user.role == 'DEVELOPER':
                return redirect('developer_dashboard')

            else:
                return redirect('dashboard')

    return render(
        request,
        'accounts/login.html'
    )
    


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

    member_loans = Loan.objects.filter(
    member=request.user
    ).order_by('-id')

    member_deposits = DepositRequest.objects.filter(
    member=request.user
    ).order_by('-submitted_at')

    total_shares = sum(
    transaction.shares
    for transaction in ShareTransaction.objects.filter(
        member=request.user
    )
    )

    locked_shares = sum(
    loan.locked_shares
    for loan in Loan.objects.filter(
        member=request.user,
        status='APPROVED'
    )
    )

    share_value = total_shares * 5000

    available_shares = (
    total_shares - locked_shares
    )

    active_loans = Loan.objects.filter(
    member=request.user,
    status='APPROVED'
    ).count()

    context = {
        'membership': membership,
        'total_shares': total_shares,
        'locked_shares': locked_shares,
        'available_shares': available_shares,
        'savings_value': savings_value,
        'available_loan': available_loan,
        'member_loans': member_loans,
        'member_deposits': member_deposits,
        'share_value': share_value,
        'active_loans': active_loans,
    }

    return render(
        request,
        'accounts/dashboard.html',
        context
    )

   


@login_required
def admin_dashboard(request):

    if request.user.role != 'ADMINISTRATOR':
        return render(
            request,
            'accounts/access_denied.html'
        )

    total_users = User.objects.count()

    total_members = User.objects.filter(
        role='MEMBER'
    ).count()

    finance_officers = User.objects.filter(
        role='FINANCE'
    ).count()

    pending_memberships = MembershipApplication.objects.filter(
        status='PENDING'
    ).count()

    pending_deposits = DepositRequest.objects.filter(
        status='PENDING'
    ).count()

    pending_loans = Loan.objects.filter(
        status='PENDING'
    ).count()

    active_loans = Loan.objects.filter(
        status='APPROVED'
    ).count()

    context = {
        'total_users': total_users,
        'total_members': total_members,
        'finance_officers': finance_officers,
        'pending_memberships': pending_memberships,
        'pending_deposits': pending_deposits,
        'pending_loans': pending_loans,
        'active_loans': active_loans,
    }

    return render(
        request,
        'accounts/admin_dashboard.html',
        context
    )


@login_required
def manage_members(request):

    members = User.objects.filter(
        role='MEMBER'
    )

    return render(
        request,
        'accounts/manage_members.html',
        {
            'members': members
        }
    )

@login_required
def member_detail(request, user_id):

    member = get_object_or_404(
        User,
        id=user_id
    )

    shares = ShareTransaction.objects.filter(
        member=member
    )

    deposits = DepositRequest.objects.filter(
        member=member
    )

    loans = Loan.objects.filter(
        member=member
    )

    repayments = LoanRepayment.objects.filter(
        loan__member=member
    )
    total_shares = shares.count()

    total_deposits = deposits.filter(
    status='APPROVED'
    ).count()

    total_loans = loans.count()

    total_repayments = repayments.count()

    context = {
        'member': member,
        'shares': shares,
        'deposits': deposits,
        'loans': loans,
        'repayments': repayments,
        'total_shares': total_shares,
        'total_deposits': total_deposits,
        'total_loans': total_loans,
        'total_repayments': total_repayments,
        
    }

    return render(
        request,
        'accounts/member_detail.html',
        context
    )

@login_required
def manage_members(request):

    query = request.GET.get('q')

    members = User.objects.filter(
        role='MEMBER'
    )

    if query:

        members = members.filter(
            username__icontains=query
        )

    return render(
        request,
        'accounts/manage_members.html',
        {
            'members': members,
            'query': query
        }
    )

@login_required
def manage_users(request):

    users = User.objects.all().order_by('username')

    return render(
        request,
        'accounts/manage_users.html',
        {
            'users': users
        }
    )

@login_required
def change_role(
    request,
    user_id,
    role
):

    user = get_object_or_404(
        User,
        id=user_id
    )

    user.role = role
    user.save()

    return redirect(
        'manage_users'
    )

@login_required
def toggle_user_status(request, user_id):

    if request.user.role != 'ADMINISTRATOR':
        return render(
            request,
            'accounts/access_denied.html'
        )

    user = get_object_or_404(
        User,
        id=user_id
    )

    user.is_active = not user.is_active

    user.save()

    return redirect(
        'manage_users'
    )

@login_required
def manage_announcements(request):

    if request.user.role != 'ADMINISTRATOR':
        return render(
            request,
            'accounts/access_denied.html'
        )

    announcements = Announcement.objects.all().order_by(
        '-created_at'
    )
    

    return render(
        request,
        'accounts/manage_announcements.html',
        {
            'announcements': announcements
        }
    )

class AnnouncementForm(ModelForm):

    class Meta:

        model = Announcement

        fields = [
            'title',
            'image',
            'description'
        ]

@login_required
def add_announcement(request):

    if request.user.role != 'ADMINISTRATOR':
        return render(
            request,
            'accounts/access_denied.html'
        )

    if request.method == 'POST':

        form = AnnouncementForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            form.save()

            users = User.objects.all()

            for user in users:

             Notification.objects.create(
                user=user,
                title='New Announcement',
                message=f'New announcement: {announcement.title}'
                )

            return redirect(
                'announcements'
            )

    else:

        form = AnnouncementForm()

    return render(
        request,
        'accounts/add_announcement.html',
        {
            'form': form
        }
    )

def announcements(request):

    announcements = Announcement.objects.order_by(
        '-created_at'
    )

    return render(
        request,
        'accounts/announcements.html',
        {
            'announcements': announcements
        }
    )

def announcement_detail(
    request,
    announcement_id
):

    announcement = get_object_or_404(
        Announcement,
        id=announcement_id
    )

    return render(
        request,
        'accounts/announcement_detail.html',
        {
            'announcement': announcement
        }
    )

def meet_team(request):

    return render(
        request,
        'meet_team.html'
    )

@login_required
def edit_announcement(request, announcement_id):

    if request.user.role != 'ADMINISTRATOR':
        return redirect('announcements')

    announcement = Announcement.objects.get(
        id=announcement_id
    )

    if request.method == 'POST':

        announcement.title = request.POST.get('title')
        announcement.description = request.POST.get('description')

        if request.FILES.get('image'):
            announcement.image = request.FILES.get('image')

        announcement.save()

        return redirect('announcements')

    return render(
        request,
        'accounts/edit_announcement.html',
        {
            'announcement': announcement
        }
    )

@login_required
def delete_announcement(request, announcement_id):

    if request.user.role != 'ADMINISTRATOR':
        return redirect('announcements')

    announcement = Announcement.objects.get(
        id=announcement_id
    )

    announcement.delete()

    return redirect('announcements')

@login_required
def apply_membership(request):

    if request.user.role != 'USER':
        return redirect('dashboard')

    # existing code

@login_required
def profile(request):

    total_savings = DepositRequest.objects.filter(
        member=request.user,
        status='APPROVED'
    ).count()

    active_loans = Loan.objects.filter(
        member=request.user,
        status='APPROVED'
    ).count()

    context = {
        'total_savings': total_savings,
        'active_loans': active_loans,
    }

    return render(
        request,
        'accounts/profile.html',
        context
    )

@login_required
def edit_profile(request):

    if request.method == 'POST':

        form = ProfileUpdateForm(
            request.POST,
            request.FILES,
            instance=request.user
        )

        if form.is_valid():

            form.save()

            return redirect('profile')

    else:

        form = ProfileUpdateForm(
            instance=request.user
        )

    return render(
        request,
        'accounts/edit_profile.html',
        {
            'form': form
        }
    )




@login_required
def developer_dashboard(request):

    if request.user.role != 'DEVELOPER':

        return render(
            request,
            'accounts/access_denied.html'
        )

    total_users = User.objects.count()

    total_admins = User.objects.filter(
        role='ADMINISTRATOR'
    ).count()

    total_finance = User.objects.filter(
        role='FINANCE'
    ).count()

    total_members = User.objects.filter(
        role='MEMBER'
    ).count()

    total_announcements = Announcement.objects.count()

    total_membership_requests = MembershipApplication.objects.count()

    total_deposits = DepositRequest.objects.count()

    total_loans = Loan.objects.count()

    context = {

        'total_users': total_users,
        'total_admins': total_admins,
        'total_finance': total_finance,
        'total_members': total_members,

        'debug_mode': settings.DEBUG,
        'django_version': '6.1',
        'total_announcements': total_announcements,
        'total_membership_requests': total_membership_requests,
        'total_deposits': total_deposits,
        'total_loans': total_loans,

    }

    return render(
        request,
        'accounts/developer_dashboard.html',
        context
    )