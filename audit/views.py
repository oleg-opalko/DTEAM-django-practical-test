from django.shortcuts import render
from .models import RequestLog

# Create your views here.

def recent_requests(request):
    logs = RequestLog.objects.all()[:10]  # Get 10 most recent logs
    return render(request, 'audit/recent_requests.html', {'logs': logs})
