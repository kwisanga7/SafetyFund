from django.urls import path
from .views import activity_logs

urlpatterns = [

    path(
        'activity-logs/',
        activity_logs,
        name='activity_logs'
    ),

]