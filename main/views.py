from django.shortcuts import render, get_object_or_404
from django.template.loader import get_template
from django.http import HttpResponse
from .models import CV
import io
from xhtml2pdf import pisa

# Create your views here.

def index(request):
    cvs = CV.objects.all()
    print(cvs)
    return render(request, 'index.html', {'cvs': cvs})

def cv_detail(request, cv_id):
    cv = get_object_or_404(CV.objects.filter(id=cv_id))
    return render(request, 'cv_detail.html', {'cv': cv})

def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return result.getvalue()
    return None

def render_pdf_view(request, cv_id):
    cv = get_object_or_404(CV, id=cv_id)
    context = {
        'cv': cv
    }
    pdf = render_to_pdf('cv_pdf.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{cv.first_name}_{cv.last_name}_CV.pdf"'
        return response
    return HttpResponse("Error generating PDF", status=500)