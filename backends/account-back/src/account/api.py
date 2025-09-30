from typing import Optional
from ninja import Router
from ninja_jwt.authentication import JWTAuth

from shared.service.response import ResponseService
from account import schema, service as acc_svc, command as acc_cmd

router = Router()


@router.post('/register', auth=None)
def register(request, user_data: schema.RegisterSchemaIn):
    try:
        command = acc_cmd.CreateUserCommand(**user_data.dict())
        handler = acc_cmd.UserCommandHandler()
        user = handler.handle(command)
        return ResponseService.success(
            message='ثبت نام موفق!',
            data={
                'mobile': user.mobile,
                'role': user.get_role_display()
            },
            status_code=201
        )
    except Exception as e:
        return ResponseService.error(
                message='ثبت نام ناموفق!',
                errors={'detail': str(e)},
                status_code=400
            )
    
@router.post('/login', auth=None)
def login(request, user_data: schema.LoginSchemaIn):
    try:
        service = acc_svc.AuthService()
        user = service.login(**user_data.dict())
        return ResponseService.success(
                message='ورود موفق!',
                data={
                    'access': user.get('access'),
                    'refresh': user.get('refresh'),
                    'mobile': user.get('mobile'),
                },
                status_code=200,
            )
    except Exception as e:
        return ResponseService.error(
                message='ورود ناموفق!',
                errors={'detail': str(e)},
                status_code=400
            )
    
@router.post('/logout', auth=None)
def logout(request, token_data: schema.LogoutSchemaIn):
    try:
        service = acc_svc.AuthService()
        success = service.logout(request, token_data.refresh)
        if not success:
            return ResponseService.error(
                message='خطا در خروج',
                errors={'detail': 'توکن نامعتبر است.'},
                status_code=400
            )
            
        return ResponseService.success(
            message='خروج موفق!',
            data=None,
            status_code=200
        )
    except Exception as e:
        return ResponseService.error(
            message='خطای سرور',
            errors={'detail': str(e)},
            status_code=500
        )

@router.post('/create/Student/profile', auth=JWTAuth())
def create_student_profile(request, user_data: schema.CreateStudentProfileSchemaIn):
    try:
        user = request.auth
        command = acc_cmd.CreateStudentProfileCommand(user=user, **user_data.dict())
        handler = acc_cmd.StudentProfileCommandHandler()
        profile  = handler.handle(command)
        return ResponseService.success(
            message='پروفایل دانش آموز با موفقیت ساخته شد.',
            data={
                'user': user.mobile,
                'role': user.get_role_display()
            },
            status_code=201
        )
    except Exception as e:
        return ResponseService.error(
                message='ساخت پروفایل دانش آموز با مشکل مواجه شد!',
                errors={'detail': str(e)},
                status_code=400
            )
      
@router.post('/create/Teacher/profile', auth=JWTAuth())
def create_teacher_profile(request, user_data: schema.CreateTeacherProfileSchemaIn):
    try:
        user = request.auth
        command = acc_cmd.CreateTeacherProfileCommand(user=user, **user_data.dict())
        handler = acc_cmd.TeacherProfileCommandHandler()
        Teacher  = handler.handle(command)
        return ResponseService.success(
            message='پروفایل دکتر با موفقیت ساخته شد.',
            data={
                'user': user.mobile,
                'role': user.get_role_display()
            },
            status_code=201
        )
    except Exception as e:
        return ResponseService.error(
                message='ساخت پروفایل دکتر با مشکل مواجه شد!',
                errors={'detail': str(e)},
                status_code=400
            )
    

# @router.put("/{user_id}", response=UserOut)
# def update_user(request, user_id: int, payload: UserIn):
#     command = UpdateUserCommand(user_id=user_id, **payload.dict())
#     handler = UserCommandHandler()
#     user = handler.handle(command)
#     return UserOut.from_orm(user)

# # Query endpoints
# @router.get("/{user_id}", response=UserOut)
# def get_user(request, user_id: int):
#     query = GetUserByIdQuery(user_id=user_id)
#     handler = UserQueryHandler()
#     user = handler.handle(query)
#     return UserOut.from_orm(user)

# @router.get("/", response=list[UserOut])
# def list_users(request, email: Optional[str] = None, search: Optional[str] = None):
#     if email:
#         query = GetUserByMobileQuery(email=email)
#     elif search:
#         query = SearchUsersQuery(search_term=search)
#     else:
#         query = GetUserByIdQuery(user_id=0)  # Will return None
    
#     handler = UserQueryHandler()
#     users = handler.handle(query)
#     if not users:
#         return []
#     return [UserOut.from_orm(user) for user in (users if isinstance(users, list) else [users])]