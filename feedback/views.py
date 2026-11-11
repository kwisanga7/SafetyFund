from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.urls import reverse

from .forms import (
    FeedbackForm,
    FeedbackReviewForm,
    FeedbackCommentForm
)

from .models import Feedback
from notifications.services import notify_roles, notify_users


User = get_user_model()


@login_required
def create_feedback(request):

    if request.method == 'POST':
        form = FeedbackForm(request.POST)

        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.created_by = request.user
            feedback.save()

            notify_roles(
                ['ADMINISTRATOR', 'DEVELOPER'],
                title='New feedback submitted',
                message=f'{request.user.username} submitted: {feedback.title}',
                link=reverse(
                    'feedback_detail',
                    kwargs={'pk': feedback.pk},
                ),
                exclude=request.user,
            )

            return redirect('my_feedback')

    else:
        form = FeedbackForm()

    return render(
        request,
        'feedback/create_feedback.html',
        {
            'form': form
        }
    )


@login_required
def my_feedback(request):

    feedbacks = Feedback.objects.filter(
        created_by=request.user
    ).order_by('-created_at')

    return render(
        request,
        'feedback/my_feedback.html',
        {
            'feedbacks': feedbacks
        }
    )


@login_required
def feedback_detail(request, pk):

    feedback = get_object_or_404(
        Feedback,
        pk=pk
    )

    # Only the person who created the feedback,
    # Admin, or Developer can view it.
    if (
        request.user != feedback.created_by
        and request.user.role not in [
            'ADMINISTRATOR',
            'DEVELOPER'
        ]
    ):
        return render(
            request,
            'feedback/access_denied.html'
        )

    # ------------------------------------------------
    # ADMIN / DEVELOPER ACTIONS
    # ------------------------------------------------

    if request.method == 'POST':

        # Add comment
        if request.POST.get('action') == 'comment':

            comment_form = FeedbackCommentForm(
                request.POST
            )

            if comment_form.is_valid():

                comment = comment_form.save(
                    commit=False
                )

                comment.feedback = feedback
                comment.user = request.user

                comment.save()

                notify_users(
                    [feedback.created_by, feedback.assigned_to],
                    title='New feedback comment',
                    message=f'{request.user.username} commented on “{feedback.title}”.',
                    link=reverse(
                        'feedback_detail',
                        kwargs={'pk': feedback.pk},
                    ),
                    exclude=request.user,
                )

                return redirect(
                    'feedback_detail',
                    pk=feedback.pk
                )

        # Update feedback
        elif (
            request.POST.get('action') == 'update'
            and request.user.role in [
                'ADMINISTRATOR',
                'DEVELOPER'
            ]
        ):

            review_form = FeedbackReviewForm(
                request.POST,
                instance=feedback
            )

            if review_form.is_valid():
                previous_status = feedback.status
                previous_priority = feedback.priority
                previous_assignee_id = feedback.assigned_to_id
                feedback = review_form.save()

                updates = []
                if feedback.status != previous_status:
                    updates.append(
                        f'status changed to {feedback.get_status_display()}'
                    )
                if feedback.priority != previous_priority:
                    updates.append(
                        f'priority changed to {feedback.get_priority_display()}'
                    )
                if feedback.assigned_to_id != previous_assignee_id:
                    if feedback.assigned_to:
                        updates.append(
                            f'assigned to {feedback.assigned_to.username}'
                        )
                    else:
                        updates.append('assignment removed')

                if updates:
                    notify_users(
                        [feedback.created_by, feedback.assigned_to],
                        title='Feedback updated',
                        message=f'{feedback.title}: {", ".join(updates)}.',
                        link=reverse(
                            'feedback_detail',
                            kwargs={'pk': feedback.pk},
                        ),
                        exclude=request.user,
                    )

                return redirect(
                    'feedback_detail',
                    pk=feedback.pk
                )

    # ------------------------------------------------
    # REVIEW FORM
    # ------------------------------------------------

    review_form = None

    if request.user.role in [
        'ADMINISTRATOR',
        'DEVELOPER'
    ]:

        review_form = FeedbackReviewForm(
            instance=feedback
        )

        # Only Admin and Developer users
        # should appear in assignment list.
        review_form.fields[
            'assigned_to'
        ].queryset = User.objects.filter(
            role__in=[
                'ADMINISTRATOR',
                'DEVELOPER'
            ]
        )

    # ------------------------------------------------
    # COMMENT FORM
    # ------------------------------------------------

    comment_form = FeedbackCommentForm()

    # ------------------------------------------------
    # COMMENTS
    # ------------------------------------------------

    comments = feedback.comments.all().order_by(
    'created_at'
)

    return render(
        request,
        'feedback/feedback_detail.html',
        {
            'feedback': feedback,
            'review_form': review_form,
            'comment_form': comment_form,
            'comments': comments
        }
    )


@login_required
def admin_feedback(request):

    if request.user.role != 'ADMINISTRATOR':
        return render(
            request,
            'feedback/access_denied.html'
        )

    feedbacks = Feedback.objects.all().order_by(
        '-created_at'
    )

    return render(
        request,
        'feedback/admin_feedback.html',
        {
            'feedbacks': feedbacks
        }
    )


@login_required
def developer_feedback(request):

    if request.user.role != 'DEVELOPER':
        return render(
            request,
            'feedback/access_denied.html'
        )

    feedbacks = Feedback.objects.all().order_by(
        '-created_at'
    )

    return render(
        request,
        'feedback/developer_feedback.html',
        {
            'feedbacks': feedbacks
        }
    )
