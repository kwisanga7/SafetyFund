from django.contrib.auth.decorators import login_required
from .forms import MembershipApplicationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
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