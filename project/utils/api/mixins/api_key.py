from django.http import JsonResponse
from apps.config.models.api_key import APIKey

class APIKeyMixin:
    """
    Mixin to handle API key validation.
    Provides control over whether external API keys are allowed.
    """
    allow_external = False  # Default value


    def dispatch(self, request, *args, **kwargs):
        """
        Override dispatch method to check API keys before processing the request.
        Denies access based on the API key and whether external keys are allowed.
        """
        api_key = request.headers.get('API-KEY')

        if not api_key:
            return JsonResponse({'error': 'API key required'}, status=401)

        try:
            api_key_instance = APIKey.objects.get(key=api_key, is_active=True)
            request.api_key = api_key_instance  # Store the API key for future use

        except APIKey.DoesNotExist:
            return JsonResponse({'error': 'Unauthorized'}, status=401)

        if not self.allow_external and api_key_instance.is_external:
            return JsonResponse({'error': 'Unauthorized'}, status=401)
        
        return super().dispatch(request, *args, **kwargs)