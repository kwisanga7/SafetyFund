from django.contrib import admin
from .models import ShareTransaction, Loan
from .models import LoanRepayment
from .models import DepositRequest



admin.site.register(ShareTransaction)
admin.site.register(Loan)
admin.site.register(LoanRepayment)
admin.site.register(DepositRequest)