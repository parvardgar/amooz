from typing import List, Optional, Literal
from datetime import date, time
from ninja import Schema, ModelSchema
from ninja.errors import ValidationError
from pydantic import field_validator, Field, BaseModel
from decimal import Decimal


class RegisterSchemaIn(Schema):
    mobile: str = Field(..., min_length=11, max_length=11)
    first_name: str
    last_name: str
    role: Literal[0, 1, 2, 3, 4, 5, 6] 
    password: str
    password_confirm: str

    @field_validator('password_confirm')
    def passwords_match(cls, value, values, **kwargs):
        if 'password' in values.data and value != values.data['password']:
            raise ValueError('رمزعبور و تایید آن برابر نیستند!')
        return value


class LoginSchemaIn(Schema):
    mobile: str = Field(..., min_length=11, max_length=11)
    password: str = Field(..., min_length=8)


class LogoutSchemaIn(Schema):
    refresh: str  


class BaseProfileSchema(Schema):
    nation_code: Optional[str] = None
    birth_date: Optional[date] = None
    gender: Optional[int] = 2  # Default to NOTSET
    home_address: Optional[str] = None
    
    @staticmethod
    def validate_gender(value: int) -> int:
        if value not in [0, 1, 2]:
            raise ValueError("Gender must be 0 (Female), 1 (Male), or 2 (NotSet)")
        return value

    @staticmethod
    def validate_nation_code(value: str) -> str:
        if value and len(value) > 10:
            raise ValueError("Nation code must be 10 characters or less")
        return value
    

class CreateStudentProfileSchemaIn(BaseProfileSchema):
    school_address: Optional[str] = None
    school_name: Optional[str] = None
    grade: Optional[str]
    last_year_avg: Optional[float] 


class GetStudentProfileSchemaOut(BaseProfileSchema):
    school_address: Optional[str] = None
    school_name: Optional[str] = None
    grade: Optional[str] 
    consecutive_login_days: Optional[int] = None


class UpdateStudentProfileSchemaIn(BaseProfileSchema):
    school_address: Optional[str] = None
    school_name: Optional[str] = None
    grade: Optional[str] 
    consecutive_login_days: Optional[int] = None 


class CreateTeacherProfileSchemaIn(Schema):
    license_number: Optional[str] = None
    specialization: Optional[str] = None
    education: Optional[str] = None  
    experience_years: Optional[int] = None
    department: Optional[str] = None
    consultation_fee: Optional[Decimal] = None
    day: Optional[str] = None
    start: Optional[time] = None
    end: Optional[time] = None

    @field_validator('day')
    def validate_day(cls, day):
        valid_days = {'MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN'}
        if day not in valid_days:
            raise ValueError("Day must be a 3-letter weekday (e.g., 'MON')")
        return day
    
    @field_validator('end')
    def validate_time_range(cls, end, values):
        if 'start' in values and end <= values['start']:
            raise ValueError("End time must be after start time")
        return end







# Fully Validated
class ConsultantProfileSchemaIn(Schema):
    specialization: str = Field(..., min_length=4, max_length=64)
    years_of_experience: int = Field(..., gt=0, le=20)
    bio: Optional[str] = None
    education: Optional[str] = None
    languages: List[str] = []
    available_hours: dict = {}
    consultation_fee: Decimal = Field(..., max_digits=2, decimal_places=1)


# Fully Validated
class ExpertProfileSchemaIn(Schema):
    area_of_expertise: str = Field(..., min_length=4, max_length=64)
    certifications: List[str] = []
    experience_summary: str = Field(..., min_length=4, max_length=64)
    hourly_rate: Decimal = Field(..., max_digits=2, decimal_places=1)
    available_for_projects: bool = True
    skills: List[str] = []
    portfolio_link: Optional[str] = None
