from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import Notification


@login_required
def notifications_list(request):

    notifications = Notification.objects.filter(
        user=request.user
    )

    notifications.filter(
        is_read=False
    ).update(
        is_read=True
    )

    return render(
        request,
        'notifications/notifications.html',
        {
            'notifications': notifications
        }
    )