from django.urls import path
from .views import notifications_list

urlpatterns = [

    path(
        'notifications/',
        notifications_list,
        name='notifications'
    ),

]