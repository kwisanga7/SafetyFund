from django.urls import path
from .views import (
    mark_all_notifications_read,
    mark_notification_read,
    notifications_list,
)

urlpatterns = [
    path(
        'notifications/',
        notifications_list,
        name='notifications'
    ),
    path(
        'notifications/mark-all-read/',
        mark_all_notifications_read,
        name='mark_all_notifications_read',
    ),
    path(
        'notifications/<int:notification_id>/read/',
        mark_notification_read,
        name='mark_notification_read',
    ),
]
