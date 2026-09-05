from django.contrib.auth.decorators import login_required
from .forms import MembershipApplicationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import MembershipApplication
from notifications.models import Notification
from activitylogs.models import ActivityLog
from django.shortcuts import render, get_object_or_404
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

            admins = User.objects.filter(
              role='ADMINISTRATOR'
              )

            for admin in admins:

             Notification.objects.create(
             user=admin,
                title='New Membership Application',
                message=f'{request.user.username} submitted a membership application.'
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

    Notification.objects.create(
    user=application.user,
    title='Membership Approved',
    message='Congratulations! Your membership application has been approved.'
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