from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from .models import BlacklistedAccessToken


class BlacklistAccessTokenMiddleware(MiddlewareMixin):
    def process_request(self, request):
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            access_token = auth_header.split(' ')[1]
            if BlacklistedAccessToken.objects.filter(token=access_token).exists():
                return JsonResponse(
                    {'detail': 'Access token in blacklist, re-login', 'code': 401},
                    status=401
                )
        else:
            access_token = None
