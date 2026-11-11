from django.contrib.auth import get_user_model

from .models import Notification


def notify_user(user, *, title, message, link=''):
    """Create a notification for one active user."""
    if user is None or not user.is_active:
        return None

    return Notification.objects.create(
        user=user,
        title=title,
        message=message,
        link=link,
    )


def notify_users(users, *, title, message, link='', exclude=None):
    """Create notifications for active users, avoiding duplicate recipients."""
    excluded_id = getattr(exclude, 'pk', None)
    seen_ids = set()
    notifications = []

    for user in users:
        if (
            user is None
            or not user.is_active
            or user.pk == excluded_id
            or user.pk in seen_ids
        ):
            continue

        seen_ids.add(user.pk)
        notifications.append(Notification(
            user=user,
            title=title,
            message=message,
            link=link,
        ))

    return Notification.objects.bulk_create(notifications)


def notify_roles(roles, *, title, message, link='', exclude=None):
    """Notify active users whose account roles match the event audience."""
    User = get_user_model()
    users = User.objects.filter(is_active=True, role__in=roles)
    if exclude is not None:
        users = users.exclude(pk=exclude.pk)

    return notify_users(
        users,
        title=title,
        message=message,
        link=link,
        exclude=exclude,
    )


def notify_everyone(*, title, message, link='', exclude=None):
    """Notify every active account, regardless of role."""
    User = get_user_model()
    users = User.objects.filter(is_active=True)

    return notify_users(
        users,
        title=title,
        message=message,
        link=link,
        exclude=exclude,
    )
