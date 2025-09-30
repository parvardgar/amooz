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