from django.urls import path

from .views import (
    apply_membership,
    review_memberships,
    approve_membership,
    reject_membership,
)

urlpatterns = [

    path(
        'apply-membership/',
        apply_membership,
        name='apply_membership'
    ),

    path(
        'review-memberships/',
        review_memberships,
        name='review_memberships'
    ),

    path(
        'approve-membership/<int:application_id>/',
        approve_membership,
        name='approve_membership'
    ),

    path(
        'reject-membership/<int:application_id>/',
        reject_membership,
        name='reject_membership'
    ),
]