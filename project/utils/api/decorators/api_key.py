# decorators.py
from functools import wraps
from django.http import JsonResponse
from apps.config.models.api_key import APIKey

def require_api_key(allow_external=False):
    """
    Decorator to require an API key for accessing the view.
    
    Parameters:
    allow_external (bool): If True, both internal and external API keys are allowed.
                           If False, only internal API keys are allowed.
    
    Usage:
    @require_api_key(allow_external=True)
    def some_view(request):
        ...
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            api_key = request.headers.get('API-KEY')

            if not api_key:
                return JsonResponse({'error': 'API key required'}, status=401)

            try:
                api_key_instance = APIKey.objects.get(key=api_key, is_active=True)
                request.api_key = api_key_instance  # Store the API key for future use
            except APIKey.DoesNotExist:
                return JsonResponse({'error': 'Unauthorized'}, status=401)

            if not allow_external and api_key_instance.is_external:
                return JsonResponse({'error': 'Unauthorized'}, status=401)

            return view_func(request, *args, **kwargs)

        return _wrapped_view
    return decorator
