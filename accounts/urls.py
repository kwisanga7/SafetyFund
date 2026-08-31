from django.urls import path


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
    meet_team
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
]