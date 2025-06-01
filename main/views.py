from django.shortcuts import render, get_object_or_404
from .models import CV

# Create your views here.

def index(request):
    cvs = CV.objects.all()
    print(cvs)
    return render(request, 'index.html', {'cvs': cvs})

def cv_detail(request, cv_id):
    cv = get_object_or_404(CV.objects.filter(id=cv_id))
    return render(request, 'cv_detail.html', {'cv': cv})