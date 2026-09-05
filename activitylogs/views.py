from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import ActivityLog


@login_required
def activity_logs(request):

    logs = ActivityLog.objects.order_by(
        '-created_at'
    )

    return render(
        request,
        'activitylogs/activity_logs.html',
        {
            'logs': logs
        }
    )