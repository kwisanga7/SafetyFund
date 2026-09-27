from django.db import models
from django.conf import settings

class Feedback(models.Model):

    ISSUE_TYPES = [
        ('BUG', 'Bug Report'),
        ('SUGGESTION', 'Suggestion'),
        ('COMPLAINT', 'Complaint'),
        ('FEATURE', 'Feature Request'),
        ('QUESTION', 'Question'),
    ]

    STATUS_CHOICES = [
        ('OPEN', 'Open'),
        ('REVIEW', 'Under Review'),
        ('PROGRESS', 'In Progress'),
        ('RESOLVED', 'Resolved'),
        ('CLOSED', 'Closed'),
    ]

    PRIORITY_CHOICES = [
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
        ('URGENT', 'Urgent'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()

    issue_type = models.CharField(
        max_length=20,
        choices=ISSUE_TYPES
    )

    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default='LOW'
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='OPEN'
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_feedback'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class FeedbackComment(models.Model):

    feedback = models.ForeignKey(
        Feedback,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    comment = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.user.username} - {self.feedback.title}"