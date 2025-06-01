from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import get_template
from django.http import HttpResponse
from .models import CV
from rest_framework import viewsets
from .serializers import CVSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.contrib import messages
from .tasks import send_cv_pdf_email
from .utils import generate_pdf


def index(request):
    cvs = CV.objects.all()
    return render(request, 'index.html', {'cvs': cvs})

def cv_detail(request, cv_id):
    cv = get_object_or_404(CV, id=cv_id)
    return render(request, 'cv_detail.html', {'cv': cv})

def cv_pdf(request, cv_id):
    cv = get_object_or_404(CV, id=cv_id)
    pdf = generate_pdf(cv)
    
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{cv.first_name}_{cv.last_name}_CV.pdf"'
        return response
    return HttpResponse("Error generating PDF", status=500)

def settings_view(request):
    return render(request, 'settings.html')

def send_cv_email(request, cv_id):
    if request.method == 'POST':
        email = request.POST.get('email')
        cv = get_object_or_404(CV, id=cv_id)
        
        # Trigger Celery task
        send_cv_pdf_email.delay(cv.id, email)
        
        messages.success(request, f'CV will be sent to {email} shortly.')
        return redirect('cv_detail', cv_id=cv.id)
    
    return redirect('cv_detail', cv_id=cv_id)

class CVViewSet(viewsets.ModelViewSet):
    queryset = CV.objects.all()
    serializer_class = CVSerializer