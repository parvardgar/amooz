from django.http import JsonResponse
from typing import Any, Dict

class ResponseService:
    @staticmethod
    def success(
        data: Dict[str, Any] = None,
        message: str = None,
        status_code: int = 200,
    ) -> Dict[str, Any]:
        """Standard success response"""
        return JsonResponse(
            {
                "success": True,
                "message": message,
                "data": data,
                "errors": None,
            },
        status=status_code,
    )

    @staticmethod
    def success_token(
        data: Dict[str, Any] = None,
        message: str = None,
        status_code: int = 200,
    ) -> Dict[str, Any]:
        """Standard success response"""
        access = data.pop('access')
        refresh = data.pop('refresh')
        response = JsonResponse(
                {
                    "success": True,
                    "message": message,
                    "data": data,
                    "errors": None,
                },
            status=status_code,
        )
        response.set_cookie(
            key='access',
            value=access,
            httponly=True,
            secure=False,   # change to True with HTTPS Production
            samesite='Strict',
            max_age=60 * 15,  # 5 minutes
        )
        response.set_cookie(
            key='refresh',
            value=refresh,
            httponly=True,
            secure=False,   # change to True with HTTPS Production
            samesite='Strict',
            max_age=60 * 60 * 24 * 7,  # 7 days
        )
        return response

    @staticmethod
    def error(
        message: str = "An error occurred",
        errors: Dict[str, Any] = None,
        status_code: int = 400,
    ) -> Dict[str, Any]:
        """Standard error response"""
        return JsonResponse(
            {
                "success": False,
                "message": message,
                "data": None,
                "errors": errors or {},
            },
            status=status_code,
        )

    @staticmethod
    def validation_error(
        errors: Dict[str, Any],
        message: str = "Validation failed",
    ) -> JsonResponse:
        """Format validation errors (HTTP 422)"""
        return ResponseService.error(
            message=message,
            errors=errors,
            status_code=422,  # Unprocessable Entity
        )

    @staticmethod
    def not_found(
        message: str = "Resource not found",
    ) -> JsonResponse:
        """HTTP 404 response"""
        return ResponseService.error(
            message=message,
            status_code=404,
        )
    

