from django.urls import path
from . import views

urlpatterns = [

    path(
        'create/',
        views.create_feedback,
        name='create_feedback'
    ),

    path(
        'my-feedback/',
        views.my_feedback,
        name='my_feedback'
    ),

    path(
        '<int:pk>/',
        views.feedback_detail,
        name='feedback_detail'
    ),

    path(
        'admin/',
        views.admin_feedback,
        name='admin_feedback'
    ),

    path(
        'developer/',
        views.developer_feedback,
        name='developer_feedback'
    ),
]