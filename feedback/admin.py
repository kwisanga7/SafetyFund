from django.contrib import admin
from .models import Feedback

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'issue_type',
        'priority',
        'status',
        'created_by',
        'created_at'
    )

    list_filter = (
        'issue_type',
        'priority',
        'status'
    )

    search_fields = (
        'title',
        'description'
    )