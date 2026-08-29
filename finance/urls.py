from django.urls import path
from .views import request_loan, finance_dashboard


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

]