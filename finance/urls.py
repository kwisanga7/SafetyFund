from django.urls import path
from .views import request_loan

urlpatterns = [

    path(
        'request-loan/',
        request_loan,
        name='request_loan'
    ),

]