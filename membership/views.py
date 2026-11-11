from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from activitylogs.models import ActivityLog
from notifications.services import notify_roles, notify_user

from .forms import MembershipApplicationForm
from .models import MembershipApplication


@login_required
def apply_membership(request):

    if request.user.role != 'USER':
        return redirect('dashboard')

    existing_application = MembershipApplication.objects.filter(
        user=request.user,
        status='PENDING'
    ).exists()

    if existing_application:
        return redirect('dashboard')

    if request.method == 'POST':

        form = MembershipApplicationForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            application = form.save(
                commit=False
            )

            application.user = request.user

            application.save()

            ActivityLog.objects.create(
            user=request.user,
    action='Submitted membership application'
)

            notify_roles(
                ['ADMINISTRATOR', 'DEVELOPER'],
                title='New membership application',
                message=f'{request.user.username} submitted a membership application.',
                link=reverse('review_memberships'),
                exclude=request.user,
            )

            return redirect(
                'dashboard'
            )

    else:

        form = MembershipApplicationForm()

    return render(
        request,
        'membership/apply_membership.html',
        {
            'form': form
        }
    )

@login_required
def review_memberships(request):

    applications = MembershipApplication.objects.filter(
        status='PENDING'
    )

    return render(
        request,
        'membership/review_memberships.html',
        {
            'applications': applications
        }
    )

@login_required
def approve_membership(request, application_id):

    application = get_object_or_404(
        MembershipApplication,
        id=application_id
    )

    application.status = 'APPROVED'

    user = application.user
    user.role = 'MEMBER'
    user.save()

    application.save()

    ActivityLog.objects.create(
    user=request.user,
    action=f'Approved membership for {application.user.username}'
    )

    notify_user(
        application.user,
        title='Membership approved',
        message='Your membership application has been approved.',
        link=reverse('dashboard'),
    )

    return redirect(
        'review_memberships'
    )

@login_required
def reject_membership(request, application_id):

    application = get_object_or_404(
        MembershipApplication,
        id=application_id
    )

    application.status = 'REJECTED'
    application.save()

    notify_user(
        application.user,
        title='Membership application update',
        message='Your membership application was not approved. You can review your details and apply again.',
        link=reverse('apply_membership'),
    )

    return redirect(
        'review_memberships'
    )




def verify_member(request, member_number):

    membership = get_object_or_404(
        MembershipApplication,
        member_number=member_number,
        status='APPROVED'
    )

    return render(
        request,
        'membership/verify_member.html',
        {
            'membership': membership
        }
    )
