from ninja.security import HttpBearer
from ninja_jwt.authentication import JWTBaseAuthentication
from ninja.errors import AuthenticationError
from django.http import HttpRequest
import logging

logger = logging.getLogger('application')

class CookieJWTAuth(JWTBaseAuthentication, HttpBearer):
    """
    Custom JWT auth: reads token from Authorization header OR 'access' cookie.
    """

    def __call__(self, request: HttpRequest):
        auth_header = request.headers.get("Authorization", None)
        token = None
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split("Bearer ")[1]
        elif "access" in request.COOKIES:
            token = request.COOKIES.get("access")

        if not token:
            return None  # anonymous user
        return self.authenticate(request, token)

    def authenticate(self, request: HttpRequest, token: str):
        """
        This method is required by HttpBearer.
        Use JWTBaseAuthentication logic to verify token and return user.
        """
        try:
            user = self.jwt_authenticate(request, token)
            return user
        except Exception as e:
            raise AuthenticationError(str(e))
