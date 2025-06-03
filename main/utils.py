from django.template.loader import get_template
from django.http import HttpResponse
import io
from xhtml2pdf import pisa
import logging

logger = logging.getLogger(__name__)

def generate_pdf(cv):
    try:
        logger.info(f"Starting PDF generation for CV {cv.id}")
        template = get_template('cv_pdf.html')
        context = {'cv': cv}
        html = template.render(context)
        logger.info("HTML template rendered successfully")
        
        result = io.BytesIO()
        pdf = pisa.pisaDocument(io.BytesIO(html.encode("UTF-8")), result)
        
        if not pdf.err:
            logger.info("PDF generated successfully")
            return result.getvalue()
        else:
            logger.error(f"Error generating PDF: {pdf.err}")
            return None
    except Exception as e:
        logger.error(f"Exception in generate_pdf: {str(e)}")
        return None 