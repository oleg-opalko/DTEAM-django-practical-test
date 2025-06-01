from django.test import TestCase, Client
from django.urls import reverse
from .models import RequestLog

# Create your tests here.

class RequestLoggingTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_request_logging(self):
        # Make a test request
        response = self.client.get('/')
        
        # Check if log was created
        self.assertEqual(RequestLog.objects.count(), 1)
        
        # Get the log entry
        log = RequestLog.objects.first()
        
        # Verify log details
        self.assertEqual(log.method, 'GET')
        self.assertEqual(log.path, '/')
        self.assertEqual(log.status_code, 200)
        self.assertIsNotNone(log.response_time)
        self.assertIsNotNone(log.remote_ip)

    def test_recent_requests_view(self):
        # Create some test logs
        RequestLog.objects.create(
            method='GET',
            path='/test1',
            remote_ip='127.0.0.1',
            status_code=200,
            response_time=100
        )
        RequestLog.objects.create(
            method='POST',
            path='/test2',
            remote_ip='127.0.0.1',
            status_code=201,
            response_time=150
        )

        # Test the view
        response = self.client.get(reverse('audit:recent_requests'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'audit/recent_requests.html')
        self.assertEqual(len(response.context['logs']), 2)
