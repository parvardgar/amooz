from typing import List, Optional, Dict, Any

from shared.repository.base import DjangoRepository
from account import models as AccModels
    

class UserRepository(DjangoRepository[AccModels.User]):
    def __init__(self):
        super().__init__(AccModels.User)

    def get_by_mobile(self, mobile: str) -> Optional[AccModels.User]:
        return self.model_class.objects.get(mobile=mobile)
    
    def create(self, user_data: dict) -> AccModels.User:
        return self.model_class.objects.create_user(**user_data)
    
    def update(self, id: int, data: dict) -> Optional[AccModels.User]:
        user = self.get_by_id(id)
        if user is None:
            return None

        if "password" in data:
            user.set_password(data.pop("password"))  # Extract password and hash it

        if data:  # Remaining fields (if any)
            for field, value in data.items():
                setattr(user, field, value)
            user.save()
            return user
        
        user.save()
        return user
    
    def get_users_with_permission(self, permission_codename: str) -> List[AccModels.User]:
        return list(
            self.model_class.objects.filter(
                groups__permissions__codename=permission_codename
            ).distinct()
        )
    

class StudentProfileRepository(DjangoRepository[AccModels.StudentProfile]):
    def __init__(self):
        super().__init__(AccModels.StudentProfile)

    # --- Core Methods ---
    # def create(self, user: AccModels.User, **profile_data) -> AccModels.StudentProfile:
    #     """
    #     Creates a StudentProfile linked to an existing User.
    #     Example: repo.create(user_obj, {"allergies": "Pollen"})
    #     """
    #     return super().create(user=user, **profile_data)
    
    def get_by_user(self, user: AccModels.User) -> Optional[AccModels.StudentProfile]:
        """Get profile directly from User instance (uses OneToOne reverse lookup)"""
        return user.Studentprofile  # Leverages the related_name

    # --- Enhanced Utility Methods ---
    def update_medical_history(self, user_id: int, new_history: str) -> Optional[AccModels.StudentProfile]:
        """Domain-specific update method"""
        updated = self.model_class.objects.filter(user_id=user_id).update(
            medical_history=new_history
        )
        return self.get_by_id(user_id) if updated else None

    def get_all_Students_with_allergies(self) -> List[AccModels.StudentProfile]:
        """Business logic query"""
        return list(self.model_class.objects.exclude(allergies__isnull=True).exclude(allergies=""))


class TeacherProfileRepository(DjangoRepository[AccModels.TeacherProfile]):
    def __init__(self):
        super().__init__(AccModels.TeacherProfile)
    
    def create(self, user_data: dict) -> AccModels.User:
        start = user_data.pop('start')
        end = user_data.pop('end')
        return self.model_class.objects.create(time_slot=(start, end), **user_data)
    
    def get_by_license_number(self, license_number: str) -> Optional[AccModels.TeacherProfile]:
        """Get Teacher profile by license number"""
        try:
            return self.model.objects.get(license_number=license_number)
        except self.model.DoesNotExist:
            return None

    def get_by_specialization(self, specialization: str) -> List[AccModels.TeacherProfile]:
        """Get all Teachers with given specialization"""
        return list(self.model.objects.filter(specialization__iexact=specialization))

    def get_by_department(self, department: str) -> List[AccModels.TeacherProfile]:
        """Get all Teachers in a specific department"""
        return list(self.model.objects.filter(department__iexact=department))

    def get_by_availability(self, day: str) -> List[AccModels.TeacherProfile]:
        """Get Teachers available on a specific day"""
        return list(self.model.objects.filter(day=day))

    def get_by_consultation_fee_range(self, min_fee: float, max_fee: float) -> List[AccModels.TeacherProfile]:
        """Get Teachers with consultation fee within range"""
        return list(self.model.objects.filter(
            consultation_fee__gte=min_fee,
            consultation_fee__lte=max_fee
        ))

    # def search(self, query: str) -> List[AccModels.TeacherProfile]:
    #     """Search Teachers by name, specialization, or department"""
    #     return list(self.model.objects.filter(
    #         Q(user__first_name__icontains=query) |
    #         Q(user__last_name__icontains=query) |
    #         Q(specialization__icontains=query) |
    #         Q(department__icontains=query)
    #     ))