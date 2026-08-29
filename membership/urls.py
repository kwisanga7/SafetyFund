from django.urls import path
from .views import apply_membership

urlpatterns = [
    path(
        'apply-membership/',
        apply_membership,
        name='apply_membership'
    ),
]