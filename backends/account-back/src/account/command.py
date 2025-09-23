from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Optional
from django.db import transaction

from core.cqrs.base import Command, BaseCommandHandler
from src.account import repository, service, models as acc_mdl



@dataclass
class CreateUserCommand(Command):
    mobile: str
    role: int
    password: str
    password_confirm: str
    username: Optional[str] = None
    
    def __post_init__(self):
            self.username = self.mobile


@dataclass
class UpdateUserCommand(Command):
    mobile: Optional[str] = None
    username: Optional[str] = None
    email: Optional[str] = None
    is_active: Optional[bool] = None


@dataclass
class DeleteUserCommand(Command):
    mobile: str

@dataclass
class AuthUserCommand(Command):
    mobile: str
    password: str


class UserCommandHandler(BaseCommandHandler):
    def __init__(self):
        self.service = service.UserService(repository.UserRepository())
    
    @transaction.atomic
    def handle(self, command: Command):
        if isinstance(command, CreateUserCommand):
            return self._handle_create(command)
        elif isinstance(command, UpdateUserCommand):
            return self._handle_update(command)
        elif isinstance(command, DeleteUserCommand):
            return self._handle_delete(command)
        raise ValueError("Invalid command type")
    
    def _handle_create(self, command: CreateUserCommand):
        user_data = {
            'username': command.username,
            'mobile': command.mobile,
            'role': command.role,
            'password': command.password
        }
        return self.service.create_user(**user_data)

    def _handle_update(self, command: UpdateUserCommand):
        update_data = {
            k: v for k, v in command.__dict__.items()  
            if k != 'user_id' and v is not None
        }
        return self.service.update_user(command.user_id, **update_data)
    
    def _handle_delete(self, command: DeleteUserCommand):
        self.service.delete_user(command.user_id)
        return True


@dataclass
class BaseProfileCommand(Command):
    user: acc_mdl.User  # The user this profile belongs to
    nation_code: Optional[str] = None
    birth_date: Optional[date] = None
    gender: Optional[int] = 2  # Default to NOTSET
    home_address: Optional[str] = None


@dataclass
class CreateStudentProfileCommand(BaseProfileCommand):
    school_address: Optional[str] = None
    school_name: Optional[str] = None
    grade: Optional[str] 
    consecutive_login_days: Optional[int] = None 


@dataclass
class UpdateStudentProfileCommand(BaseProfileCommand):
    school_address: Optional[str] = None
    school_name: Optional[str] = None
    grade: Optional[str] 
    consecutive_login_days: Optional[int] = None 


@dataclass
class DeleteStudentProfileCommand(Command):
    user_id: int  # The user whose profile we're deleting


class StudentProfileCommandHandler(BaseCommandHandler):
    def __init__(self):
        self.service = service.StudentProfileService(repository.StudentProfileRepository())
    
    @transaction.atomic
    def handle(self, command: Command):
        if isinstance(command, CreateStudentProfileCommand):
            return self._handle_create(command)
        elif isinstance(command, UpdateStudentProfileCommand):
            return self._handle_update(command)
        elif isinstance(command, DeleteStudentProfileCommand):
            return self._handle_delete(command)
        raise ValueError("Invalid command type")
    
    def _handle_create(self, command: CreateStudentProfileCommand):
        profile_data = command.__dict__.copy()  # Create a shallow copy
        profile_data.pop('user')  # Remove the user key
        return self.service.create_profile(command.user, **profile_data)

    def _handle_update(self, command: UpdateStudentProfileCommand):
        profile_data = command.__dict__.copy()  # Create a shallow copy
        profile_data.pop('user')  # Remove the user key
        return self.service.update_profile(command.user, **profile_data)
    
    def _handle_delete(self, command: DeleteStudentProfileCommand):
        return self.service.delete_profile(command.user_id)
    

@dataclass
class CreateTeacherProfileCommand(BaseProfileCommand):
    license_number: Optional[str] = None
    specialization: Optional[str] = None
    education: Optional[str] = None
    experience_years: Optional[int] = None
    department: Optional[str] = None
    consultation_fee: Optional[Decimal] = None
    day: Optional[str] = None
    start: Optional[str] = None
    end: Optional[str] = None


@dataclass
class UpdateTeacherProfileCommand(BaseProfileCommand):
    license_number: Optional[str] = None
    specialization: Optional[str] = None
    education: Optional[str] = None
    experience_years: Optional[int] = None
    department: Optional[str] = None
    consultation_fee: Optional[Decimal] = None
    day: Optional[str] = None
    start: Optional[str] = None
    end: Optional[str] = None


@dataclass
class DeleteTeacherProfileCommand(Command):
    user_id: int  # The user whose profile we're deleting


class TeacherProfileCommandHandler(BaseCommandHandler):
    def __init__(self):
        self.service = service.TeacherProfileService(repository.TeacherProfileRepository())
    
    @transaction.atomic
    def handle(self, command: Command):
        if isinstance(command, CreateTeacherProfileCommand):
            return self._handle_create(command)
        elif isinstance(command, UpdateTeacherProfileCommand):
            return self._handle_update(command)
        elif isinstance(command, DeleteTeacherProfileCommand):
            return self._handle_delete(command)
        raise ValueError("Invalid command type")
    
    def _handle_create(self, command: CreateTeacherProfileCommand):
        profile_data = command.__dict__.copy()  # Create a shallow copy
        profile_data.pop('user')  # Remove the user key
        return self.service.create_profile(command.user, **profile_data)

    def _handle_update(self, command: UpdateTeacherProfileCommand):
        profile_data = command.__dict__.copy()  # Create a shallow copy
        profile_data.pop('user')  # Remove the user key
        return self.service.update_profile(command.user, **profile_data)
    
    def _handle_delete(self, command: DeleteTeacherProfileCommand):
        return self.service.delete_profile(command.user_id)