from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken


def is_valid_token(token):
    try:
        RefreshToken(token)
        return True
    except TokenError:
        return False
