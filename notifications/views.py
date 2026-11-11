from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

from .models import Notification


@login_required
def notifications_list(request):
    notifications = Notification.objects.filter(
        user=request.user
    )

    return render(
        request,
        'notifications/notifications.html',
        {'notifications': notifications}
    )


@login_required
@require_POST
def mark_notification_read(request, notification_id):
    notification = get_object_or_404(
        Notification,
        pk=notification_id,
        user=request.user,
    )
    notification.is_read = True
    notification.save(update_fields=['is_read'])

    if notification.link and url_has_allowed_host_and_scheme(
        notification.link,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        return redirect(notification.link)

    return redirect('notifications')


@login_required
@require_POST
def mark_all_notifications_read(request):
    Notification.objects.filter(
        user=request.user,
        is_read=False,
    ).update(is_read=True)

    return redirect('notifications')
