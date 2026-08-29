from django.contrib import admin
from .models import ShareTransaction, Loan

admin.site.register(ShareTransaction)
admin.site.register(Loan)