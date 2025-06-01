from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

from main.utils import generate_pdf
from .models import CV


@shared_task
def send_cv_pdf_email(cv_id, email):
    try:
        cv = CV.objects.get(id=cv_id)
        pdf_content = generate_pdf(cv)
        
        subject = f'CV of {cv.full_name}'
        message = f'Please find attached the CV of {cv.full_name}.'
        
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
            attachments=[('cv.pdf', pdf_content, 'application/pdf')]
        )
        return True
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return False 