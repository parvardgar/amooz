from django.db import models
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser, UserManager
from django.contrib.postgres.fields import DateTimeRangeField
from django.contrib.postgres.indexes import GinIndex
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError


class CustomUserManager(UserManager):
    use_in_migrations = True

    def _create_user(self, mobile, password, **extra_fields):
        if not mobile:
            raise ValueError('The given username must be set')
        user = self.model(mobile=mobile, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, mobile, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(mobile, password, **extra_fields)

    def create_superuser(self, mobile, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('username', mobile)
        extra_fields.setdefault('role', 5)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(mobile, password, **extra_fields)

   
class User(AbstractUser):
    STUDENT = 0
    VOLUNTEER = 1
    TEACHER = 2
    SUPER = 3
    HERO = 4
    ADMIN = 5
    ROLES = (
        (STUDENT, 'Student'),
        (VOLUNTEER, 'Volunteer'),
        (TEACHER, 'Teacher'),
        (SUPER, 'Super'),
        (HERO, 'Hero'),
        (ADMIN, 'Admin'),
    )
    mobile = models.CharField(
        max_length=11, unique=True,
    )
    role = models.PositiveSmallIntegerField(
        choices=ROLES,
        default=0
    ) 
    objects = CustomUserManager()
    USERNAME_FIELD = 'mobile'

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f'{self.mobile} ({self.get_role_display()})'


class BaseProfile(models.Model):
    FEMALE = 0
    MALE = 1
    NOTSET = 2
    GENDERS = (
        (FEMALE, 'Female'),
        (MALE, 'Male'),
        (NOTSET, 'NotSet')
    ) 
    user = models.OneToOneField(
        User,
        on_delete=models.PROTECT,
        primary_key=True,
        related_name='%(class)s'
    )
    nation_code = models.CharField(
        max_length=10, unique=True, null=True, blank=True
    )
    birth_date = models.DateField(
        null=True, blank=True
    )
    
    gender = models.PositiveSmallIntegerField(
        choices=GENDERS,
        default=2, blank=True, null=True
    )
    home_address = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class StudentProfile(BaseProfile):
    FRESHMAN = 9
    SOPHOMORE = 10
    JUNIOR = 11
    SENIOR = 12
    GRADES = (
        (FRESHMAN, 'Freshman'),
        (SOPHOMORE, 'Sophomore'),
        (JUNIOR, 'Junior'),
        (SENIOR , 'Senior')
    )
    # subjects_of_interest = models.ManyToManyField('core.Subject', blank=True)
    consecutive_login_days = models.PositiveIntegerField(default=0)
    school_address = models.TextField(blank=True, null=True)
    school_name = models.CharField(
        max_length=128, blank=True, null=True
    )
    grade = models.PositiveSmallIntegerField(
        choices=GRADES,
        null=True,
        blank=True
    )
    class Meta:
        verbose_name = 'Student Profile'
        verbose_name_plural = 'Student Profiles'
    
    def save(self, *args, **kwargs):
        if self.user.role != 0:
            raise ValidationError('Student Profile can only be linked to Student user type')
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Student:{self.user.mobile}'


class TeacherProfile(BaseProfile):
    license_number = models.CharField(max_length=64, unique=True)
    specialization = models.CharField(max_length=128)
    education = models.TextField(blank=True, null=True)
    experience_years = models.PositiveSmallIntegerField(default=0)
    department = models.CharField(max_length=128)
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    day = models.CharField(max_length=3, choices=[
        ('MON', 'Monday'),
        ('TUE', 'Tuesday'),
        ('WED', 'Wednesday'),
        ('THU', 'Thursday'),
        ('FRI', 'Friday'),
        ('SAT', 'Saturday'),
        ('SUN', 'Sunday'),
    ], null=True, blank=True)
    time_slot = DateTimeRangeField(null=True, blank=True)

    class Meta:
        verbose_name = 'Teacher Profile'
        verbose_name_plural = 'Teacher Profiles'
        indexes = [
            models.Index(fields=['day', 'time_slot']),  # Faster filtering
        ]

    def save(self, *args, **kwargs):
        if self.user.role != 3:
            raise ValidationError('Teacher Profile can only be linked to Teacher user type')
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Teacher:{self.user.mobile}'


class VolunteerProfile(BaseProfile):
    specialization = models.CharField(max_length=100, null=True, blank=True)
    years_of_experience = models.PositiveIntegerField(null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    education = models.TextField(null=True, blank=True)
    languages = models.JSONField(default=list)  
    available_hours = models.JSONField(default=dict)
    consultation_fee = models.FloatField(default=0.0)
    rating = models.FloatField(default=0.0)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f'Volunteer:{self.user.mobile}'
    
    def save(self, *args, **kwargs):
        if self.user.role != 1:
            raise ValidationError('Volunteer Profile can only be linked to Volunteer user type')
        super().save(*args, **kwargs)


# class SuperProfile(BaseProfile):
#     area_of_expertise = models.CharField(max_length=100, null=True, blank=True)
#     certifications = models.JSONField(default=list)
#     experience_summary = models.TextField(null=True, blank=True)
#     hourly_rate = models.FloatField(default=0.0)
#     available_for_projects = models.BooleanField(default=True)
#     skills = models.JSONField(default=list)
#     portfolio_link = models.URLField(blank=True, null=True)
#     is_approved = models.BooleanField(default=False)

#     def save(self, *args, **kwargs):
#         if self.user.role != 3:
#             raise ValidationError("ExpertProfile can only be linked to expert user type")
#         super().save(*args, **kwargs)

#     def __str__(self):
#         return f"Expert:{self.user.mobile}"
    

# class HeroProfile(BaseProfile):
#     area_of_expertise = models.CharField(max_length=100, null=True, blank=True)
#     certifications = models.JSONField(default=list)
#     experience_summary = models.TextField(null=True, blank=True)
#     hourly_rate = models.FloatField(default=0.0)
#     available_for_projects = models.BooleanField(default=True)
#     skills = models.JSONField(default=list)
#     portfolio_link = models.URLField(blank=True, null=True)
#     is_approved = models.BooleanField(default=False)

#     def save(self, *args, **kwargs):
#         if self.user.role != 3:
#             raise ValidationError("ExpertProfile can only be linked to expert user type")
#         super().save(*args, **kwargs)

#     def __str__(self):
#         return f"Expert:{self.user.mobile}"