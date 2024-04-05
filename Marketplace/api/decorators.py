import json
from functools import wraps
from django.http import JsonResponse

def validate_required_fields(required_fields):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            for field in required_fields:
                if field not in request.data: 
                    return JsonResponse({'error': f'Required field "{field}" is missing.'}, status=400)
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator
