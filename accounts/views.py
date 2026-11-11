import os

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.staticfiles import finders
from django.db import models
from django.forms import ModelForm
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import get_template
from django.urls import reverse
from xhtml2pdf import pisa

from activitylogs.models import ActivityLog
from feedback.models import Feedback
from finance.models import DepositRequest, Loan, LoanRepayment, ShareTransaction
from membership.models import MembershipApplication
from notifications.services import notify_everyone, notify_roles, notify_user

from .forms import ProfileUpdateForm, RegisterForm
from .models import Announcement, SiteSetting, User


def register(request):

    if request.method == 'POST':

        form = RegisterForm(request.POST)

        if form.is_valid():

            user = form.save()

            ActivityLog.objects.create(
                user=user,
                action='Registered a new account'
            )

            notify_roles(
                ['ADMINISTRATOR', 'DEVELOPER'],
                title='New account registration',
                message=f'{user.username} has registered.',
                link=reverse('manage_users'),
                exclude=user,
            )

            messages.success(
                request,
                'Account created successfully.'
            )

            return redirect('home')

        else:

            messages.error(
                request,
                'Please correct the errors below.'
            )

    else:

        form = RegisterForm()

    return render(
        request,
        'accounts/register.html',
        {
            'form': form
        }
    )


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

    pending_loans = Loan.objects.filter(
        member=request.user,
        status='PENDING'
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
        'pending_loans': pending_loans,
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

    # Feedback statistics
    feedback_total = Feedback.objects.count()

    feedback_open = Feedback.objects.filter(
     status='OPEN'
        ).count()

    feedback_review = Feedback.objects.filter(
     status='REVIEW'
       ).count()

    feedback_progress = Feedback.objects.filter(
     status='PROGRESS'
      ).count()

    context.update({
        'feedback_total': feedback_total,
        'feedback_open': feedback_open,
        'feedback_review': feedback_review,
        'feedback_progress': feedback_progress,
    })

    return render(request, 'accounts/admin_dashboard.html', context)

@login_required
def manage_members(request):
    query = request.GET.get('q')
    members = User.objects.filter(role='MEMBER')

    if query:
        members = members.filter(username__icontains=query)

    return render(
        request,
        'accounts/manage_members.html',
        {'members': members, 'query': query},
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

    previous_role = user.role
    user.role = role
    user.save(update_fields=['role'])

    if previous_role != role and user != request.user:
        notify_user(
            user,
            title='Your account role was updated',
            message=f'Your role changed from {previous_role} to {user.get_role_display()}.',
            link=reverse('profile'),
        )

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
    user.save(update_fields=['is_active'])

    if user.is_active:
        notify_user(
            user,
            title='Your account is active',
            message='An administrator has reactivated your account.',
            link=reverse('dashboard'),
        )
    else:
        notify_roles(
            ['ADMINISTRATOR', 'DEVELOPER'],
            title='Account deactivated',
            message=f'{user.username} was deactivated by {request.user.username}.',
            link=reverse('manage_users'),
            exclude=request.user,
        )

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
            announcement = form.save()
            notify_everyone(
                title='New announcement',
                message=announcement.title,
                link=reverse(
                    'announcement_detail',
                    kwargs={'announcement_id': announcement.pk},
                ),
                exclude=request.user,
            )
            return redirect('announcements')


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
        notify_everyone(
            title='Announcement updated',
            message=announcement.title,
            link=reverse(
                'announcement_detail',
                kwargs={'announcement_id': announcement.pk},
            ),
            exclude=request.user,
        )

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

    announcement_title = announcement.title
    announcement.delete()
    notify_everyone(
        title='Announcement removed',
        message=announcement_title,
        link=reverse('announcements'),
        exclude=request.user,
    )

    return redirect('announcements')

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
            changed_fields = form.changed_data
            form.save()

            if changed_fields:
                notify_roles(
                    ['ADMINISTRATOR', 'DEVELOPER'],
                    title='Member profile updated',
                    message=f'{request.user.username} updated their profile.',
                    link=reverse('member_detail', kwargs={'user_id': request.user.pk}),
                    exclude=request.user,
                )

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

    # Feedback statistics
    feedback_total = Feedback.objects.count()

    feedback_open = Feedback.objects.filter(
    status='OPEN'
    ).count()

    feedback_review = Feedback.objects.filter(
    status='REVIEW'
    ).count()

    feedback_progress = Feedback.objects.filter(
    status='PROGRESS'
).count()

    context.update({
        'feedback_total': feedback_total,
        'feedback_open': feedback_open,
        'feedback_review': feedback_review,
        'feedback_progress': feedback_progress,
    })

    return render(request, 'accounts/developer_dashboard.html', context)

@login_required
def site_settings(request):

    setting = SiteSetting.objects.first()

    if request.method == 'POST':

        setting.site_name = request.POST.get(
            'site_name'
        )

        setting.site_slogan = request.POST.get(
            'site_slogan'
        )

        setting.organization_name = request.POST.get(
            'organization_name'
        )

        setting.email = request.POST.get(
            'email'
        )

        setting.phone = request.POST.get(
            'phone'
        )

        setting.address = request.POST.get(
            'address'
        )

        setting.footer_text = request.POST.get(
            'footer_text'
        )

        setting.save()

        notify_roles(
            ['DEVELOPER'],
            title='Site settings updated',
            message=f'{request.user.username} updated the site settings.',
            link=reverse('site_settings'),
            exclude=request.user,
        )

        return redirect(
            'site_settings'
        )

    return render(
        request,
        'accounts/site_settings.html',
        {
            'setting': setting
        }
    )





@login_required
def member_id_card(request):

    membership = MembershipApplication.objects.filter(
        user=request.user,
        status='APPROVED'
    ).first()

    return render(
        request,
        'accounts/member_id_card.html',
        {
            'membership': membership
        }
    )


def link_callback(uri, rel):

    # Media files
    if uri.startswith(settings.MEDIA_URL):

        path = os.path.join(
            settings.MEDIA_ROOT,
            uri.replace(settings.MEDIA_URL, '')
        )

        return path

    # Static files
    if uri.startswith(settings.STATIC_URL):

        relative_path = uri.replace(
            settings.STATIC_URL,
            ''
        )

        path = finders.find(relative_path)

        if path:
            return path

    return uri

@login_required
def download_member_card(request):

    membership = get_object_or_404(
        MembershipApplication,
        user=request.user,
        status='APPROVED'
    )

    # Only approved members should download a card
    if request.user.role != 'MEMBER':
        return redirect('profile')

    template = get_template(
        'accounts/member_card_pdf.html'
    )

    html = template.render({
        'user': request.user,
        'membership': membership,
    })

    response = HttpResponse(
        content_type='application/pdf'
    )

    response['Content-Disposition'] = (
        f'attachment; filename="SafetyFund_{membership.member_number}.pdf"'
    )

    pisa_status = pisa.CreatePDF(
        html,
        dest=response,
        link_callback=link_callback
    )

    if pisa_status.err:
        return HttpResponse(
            'An error occurred while generating the PDF.'
        )

    return response
