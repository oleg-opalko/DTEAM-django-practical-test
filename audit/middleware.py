import time
import logging
from .models import RequestLog

logger = logging.getLogger(__name__)

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()

        try:
            response = self.get_response(request)

            response_time = (time.time() - start_time) * 1000

            try:
                RequestLog.objects.create(
                    method=request.method,
                    path=request.path,
                    query_string=request.META.get('QUERY_STRING', ''),
                    remote_ip=self.get_client_ip(request),
                    user=request.user if request.user.is_authenticated else None,
                    status_code=response.status_code,
                    response_time=response_time
                )
            except Exception as e:
                logger.error(f"Error creating request log: {str(e)}")
                pass

            return response
        except Exception as e:
            logger.error(f"Error in request processing: {str(e)}")
            raise

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip 