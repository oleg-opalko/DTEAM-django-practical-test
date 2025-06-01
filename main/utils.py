from django.template.loader import get_template
from django.http import HttpResponse
import io
from xhtml2pdf import pisa

def generate_pdf(cv):
    """
    Generate PDF from CV object
    """
    template = get_template('cv_pdf.html')
    context = {'cv': cv}
    html = template.render(context)
    
    result = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(html.encode("UTF-8")), result)
    
    if not pdf.err:
        return result.getvalue()
    return None 