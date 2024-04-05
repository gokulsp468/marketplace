from . import models

class ApiLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        request_body = request.body
        
        response = self.get_response(request)
        
        models.ApiLog.objects.create(
            api_endpoint=request.path,
            response_data=response.content.decode(),
            request_data=request_body.decode(),
            status=response.status_code
        )
        
        return response
