from django.conf import settings
from django.http import JsonResponse
from ninja_extra import NinjaExtraAPI
from ninja_jwt.controller import NinjaJWTDefaultController
from ninja.errors import ValidationError

from account.api import router as account_router


api = NinjaExtraAPI()


@api.exception_handler(ValidationError)
def custom_validation_error(request, exc: ValidationError):
    errors = {}
    for error in exc.errors:
        # field = ".".join(str(loc) for loc in error["loc"] if loc != "body") --> user_data.role
        field = error["loc"][-1]  # --> role
        custom_message = settings.CUSTOM_VALIDATION_MESSAGES.get(error['msg'])
        ctx_msg = error.get("ctx", {}).get("error")
        if custom_message:
            errors[field] = custom_message
        elif ctx_msg:
            errors[field] = ctx_msg
        else:
            errors[field] = error['msg']
    return JsonResponse(
        {
            "success": False,
            "message": "عملیات ناموفق!",
            "data": None,
            "errors": errors
        },
        status=422,
    )


api.register_controllers(NinjaJWTDefaultController)
api.add_router("accounts/auth", account_router)    # You can add a router as an object
# api.add_router("chats", "chat.api.router")     or by Python path