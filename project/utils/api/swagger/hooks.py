from drf_spectacular.utils import OpenApiParameter

def filter_endpoints(endpoints, **kwargs):
    # if request.user.is_superuser:
    #     return endpoints  # Admin kullanıcılar tüm endpointleri görsün
    # else:
        allowed_paths = [
            '/api/v1/support/products/',
            '/api/v1/support/products/{slug}/',

            '/api/v1/support/categories/',
            '/api/v1/support/categories/{slug}/',
        ]
        return [
            (path, path_regex, method, view) for path, path_regex, method, view in endpoints
            if path in allowed_paths
        ]


