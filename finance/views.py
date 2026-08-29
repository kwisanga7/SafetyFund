from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

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