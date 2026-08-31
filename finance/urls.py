from django.urls import path

from .views import (
    request_loan,
    finance_dashboard,
    pending_loans,
    approve_loan,
    reject_loan,
    mark_loan_paid,
    compliance_report,
    deposit_request,
    pending_deposits,
    approve_deposit,
    reject_deposit,
    make_repayment,
    pending_repayments,
    approve_repayment,
    reject_repayment
)


urlpatterns = [

    path(
        'request-loan/',
        request_loan,
        name='request_loan'
    ),

    path(
        'finance-dashboard/',
        finance_dashboard,
        name='finance_dashboard'
    ),

    path(
    'pending-loans/',
    pending_loans,
    name='pending_loans'
    ),

    path(
    'approve-loan/<int:loan_id>/',
    approve_loan,
    name='approve_loan'
    ),

    path(
    'reject-loan/<int:loan_id>/',
    reject_loan,
    name='reject_loan'
    ),
    path(
    'mark-paid/<int:loan_id>/',
    mark_loan_paid,
    name='mark_loan_paid'
),
path(
    'compliance-report/',
    compliance_report,
    name='compliance_report'
),
path(
    'deposit-request/',
    deposit_request,
    name='deposit_request'
),
path(
    'pending-deposits/',
    pending_deposits,
    name='pending_deposits'
),

path(
    'approve-deposit/<int:deposit_id>/',
    approve_deposit,
    name='approve_deposit'
),

path(
    'reject-deposit/<int:deposit_id>/',
    reject_deposit,
    name='reject_deposit'
),

path(
    'make-repayment/<int:loan_id>/',
    make_repayment,
    name='make_repayment'
),
path(
    'pending-repayments/',
    pending_repayments,
    name='pending_repayments'
),

path(
    'approve-repayment/<int:repayment_id>/',
    approve_repayment,
    name='approve_repayment'
),

path(
    'reject-repayment/<int:repayment_id>/',
    reject_repayment,
    name='reject_repayment'
),
path(
    'pending-deposits/',
    pending_deposits,
    name='pending_deposits'
),

path(
    'pending-loans/',
    pending_loans,
    name='pending_loans'
),

path(
    'pending-repayments/',
    pending_repayments,
    name='pending_repayments'
),

]