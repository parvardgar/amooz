from typing import Optional
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.contrib.auth import get_user_model, authenticate
from ninja_jwt.tokens import RefreshToken
from ninja_jwt.schema import TokenObtainPairInputSchema

from account import repository as acc_repo 

class AuthService:
    def login(self, **params):
        user = authenticate(
            mobile=params.get('mobile'),
            password=params.get('password')
        )
        if user is None:
            raise Exception("شماره موبایل یا رمز عبور اشتباه است")
        refresh = RefreshToken.for_user(user)
        login_data = {
            'mobile': params.get('mobile'),
            'refresh': str(refresh),
            'access': str(refresh.access_token)
            }
        return login_data

    def logout(self, request, refresh_token: str) -> bool:
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return True
        except Exception:
            return False
        
    # def set_password(self, user: User, new_password: str) -> None:
    #     """Password setting without validation"""
    #     user.set_password(new_password)
    #     self.repository.update(user)
        

class UserService:
    def __init__(self, repository: acc_repo.UserRepository):
        self.repository = repository
    
    def create_user(self, **params) -> get_user_model:
        try:
            return self.repository.get_by_mobile(params.get('mobile'))
        except ObjectDoesNotExist:
            return self.repository.create(params)
        except ValidationError as e:
            raise ValidationError(e.message_dict)
    
    def update_user(self, user_id: int, **update_data) -> Optional[get_user_model]:
        user = self.repository.get_by_id(user_id)
        if not user:
            return None
        
        for field, value in update_data.items():
            if field == 'password':
                user.set_password(value)
            else:
                setattr(user, field, value)
        
        try:
            return self.repository.update(user)
        except ValidationError as e:
            raise ValidationError(e.message_dict)
    

class StudentProfileService:
    def __init__(self, repository: acc_repo.StudentProfileRepository):
        self.repository = repository
    
    def create_profile(self, user: get_user_model, **kwargs):
        # Add any business logic/validation here
        if user.role != 0:  
            raise ValueError("Only Students can have Student profiles")
        return self.repository.create({"user": user, **kwargs})
    
    def update_profile(self, user_id: int, **kwargs):
        # Add any business logic/validation here
        return self.repository.update(user_id, **kwargs)
    
    def delete_profile(self, user_id: int):
        self.repository.delete(user_id)


class TeacherProfileService:
    def __init__(self, repository: acc_repo.TeacherProfileRepository):
        self.repository = repository
    
    def create_profile(self, user: get_user_model, **kwargs):
        # Add any business logic/validation here
        if user.role != 3:  
            raise ValueError("Only Teachers can have Teacher profiles")
        return self.repository.create({"user": user, **kwargs})
    
    def update_profile(self, user_id: int, **kwargs):
        # Add any business logic/validation here
        return self.repository.update(user_id, **kwargs)
    
    def delete_profile(self, user_id: int):
        self.repository.delete(user_id)
    