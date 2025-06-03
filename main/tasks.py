from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

from main.utils import generate_pdf
from .models import CV

logger = logging.getLogger(__name__)

@shared_task
def send_cv_pdf_email(cv_id, email):
    try:
        logger.info(f"Starting to process CV {cv_id} for email {email}")
        cv = CV.objects.get(id=cv_id)
        logger.info(f"Found CV: {cv.full_name}")
        
        pdf_content = generate_pdf(cv)
        if pdf_content is None:
            logger.error("Error: PDF generation failed")
            return False
        logger.info("PDF generated successfully")
        
        subject = f'CV of {cv.full_name}'
        message = f'Please find attached the CV of {cv.full_name}.'
        
        logger.info(f"Attempting to send email to {email}")
        logger.info(f"Using email settings: HOST={settings.EMAIL_HOST}, PORT={settings.EMAIL_PORT}, USER={settings.EMAIL_HOST_USER}")
        
        try:
            msg = MIMEMultipart()
            msg['Subject'] = subject
            msg['From'] = settings.DEFAULT_FROM_EMAIL
            msg['To'] = email
            
            msg.attach(MIMEText(message))
            
            pdf_attachment = MIMEApplication(pdf_content, _subtype='pdf')
            pdf_attachment.add_header('Content-Disposition', 'attachment', filename='cv.pdf')
            msg.attach(pdf_attachment)
            
            logger.info("Connecting to SMTP server...")
            server = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
            server.starttls()
            
            logger.info("Logging in to SMTP server...")
            server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
            
            logger.info("Sending email...")
            server.send_message(msg)
            
            # Close connection
            server.quit()
            logger.info("Email sent successfully")
            return True
            
        except smtplib.SMTPException as e:
            logger.error(f"SMTP Error: {str(e)}")
            return False
            
    except Exception as e:
        logger.error(f"Error sending email: {str(e)}")
        logger.error(f"Error type: {type(e)}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        return False