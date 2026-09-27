from django import forms
from .models import Feedback, FeedbackComment


class FeedbackForm(forms.ModelForm):

    class Meta:
        model = Feedback
        fields = [
            'title',
            'description',
            'issue_type',
            'priority'
        ]


class FeedbackReviewForm(forms.ModelForm):

    class Meta:
        model = Feedback
        fields = [
            'status',
            'priority',
            'assigned_to'
        ]

        widgets = {
            'status': forms.Select(
                attrs={
                    'class': 'form-select'
                }
            ),

            'priority': forms.Select(
                attrs={
                    'class': 'form-select'
                }
            ),

            'assigned_to': forms.Select(
                attrs={
                    'class': 'form-select'
                }
            ),
        }


class FeedbackCommentForm(forms.ModelForm):

    class Meta:
        model = FeedbackComment
        fields = [
            'comment'
        ]

        widgets = {
            'comment': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 4,
                    'placeholder': 'Write your comment...'
                }
            )
        }