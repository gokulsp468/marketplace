# from django.utils.deprecation import MiddlewareMixin
# import json
# from app import models

# class ExampleMiddleware(MiddlewareMixin):
    
#     def __init__(self, get_response):
#         self.get_response = get_response
        
#     def __call__(self, request, *args, **kwargs):
#         response = self.get_response(request)
#         print("middleware called")
#         self.log_api_request(request, response)
#         return response
        
#     def log_api_request(self, request, response):
#         # Extract relevant information from the response object
#         response_data = {
             
#             'content': response.content.decode(),
           
#         }
        
#         log_data = {
#             'method': request.method,
#             'path': request.path,
#             'query_params': dict(request.GET),
#             'response_data':response_data,
#             'status_code':response.status_code,
#         }
        
#         models.APILog.objects.create(**log_data)
