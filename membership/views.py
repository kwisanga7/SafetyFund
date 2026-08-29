from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .forms import MembershipApplicationForm


@login_required
def apply_membership(request):

    if request.method == 'POST':

        form = MembershipApplicationForm(request.POST)

        if form.is_valid():

            application = form.save(commit=False)
            application.user = request.user
            application.save()

            return redirect('dashboard')

    else:
        form = MembershipApplicationForm()

    return render(
        request,
        'membership/apply_membership.html',
        {'form': form}
    )