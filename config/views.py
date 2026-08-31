from django.shortcuts import render
from accounts.models import Announcement
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    return render(request, 'accounts/dashboard.html')





def home(request):

    latest_announcements = Announcement.objects.order_by(
        '-created_at'
    )[:3]

    context = {
        'latest_announcements': latest_announcements
    }

    return render(
        request,
        'home.html',
        context
    )



def about(request):
    return render(request, 'about.html')


def contact(request):
    return render(request, 'contact.html')