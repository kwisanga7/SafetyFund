from django.urls import path
from django.contrib.auth.views import PasswordChangeView
from django.conf import settings
from django.conf.urls.static import static

from .views import (
    register,
    login_user,
    logout_user,
    dashboard,
    admin_dashboard,
    manage_members,
    member_detail,
    manage_users,
    change_role,
    toggle_user_status,
    manage_announcements,
    add_announcement,
    announcements,
    announcement_detail,
    meet_team,
    edit_announcement,
    delete_announcement,
    profile,
    edit_profile,
    developer_dashboard,
    site_settings,
    member_id_card,
    download_member_card,
)

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
    path('admin-dashboard/',admin_dashboard,name='admin_dashboard'),
    path( 'manage-members/',manage_members,name='manage_members'),
    path( 'member/<int:user_id>/',member_detail,name='member_detail'),
    path(
    'manage-users/',
    manage_users,
    name='manage_users'
),

path(
    'change-role/<int:user_id>/<str:role>/',
    change_role,
    name='change_role'
),
path(
    'toggle-user-status/<int:user_id>/',
    toggle_user_status,
    name='toggle_user_status'
),
path(
    'admin-announcements/',
    manage_announcements,
    name='manage_announcements'
),

path(
    'add-announcement/',
    add_announcement,
    name='add_announcement'
),

path(
    'announcements/',
    announcements,
    name='announcements'
),

path(
    'announcement/<int:announcement_id>/',
    announcement_detail,
    name='announcement_detail'
),
path(
    'meet-team/',
    meet_team,
    name='meet_team'
),
path(
    'edit-announcement/<int:announcement_id>/',
    edit_announcement,
    name='edit_announcement'
),

path(
    'delete-announcement/<int:announcement_id>/',
    delete_announcement,
    name='delete_announcement'
),
path(
    'profile/',
    profile,
    name='profile'
),

path(
    'profile/edit/',
    edit_profile,
    name='edit_profile'
),


path(
    'change-password/',
    PasswordChangeView.as_view(
        template_name='accounts/change_password.html'
    ),
    name='change_password'
),
path(
    'developer-dashboard/',
    developer_dashboard,
    name='developer_dashboard'
),
path(
    'site-settings/',
    site_settings,
    name='site_settings'
),
path(
    'member-id-card/',
    member_id_card,
    name='member_id_card'
),
path(
    'download-member-card/',
    download_member_card,
    name='download_member_card'
),

]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )