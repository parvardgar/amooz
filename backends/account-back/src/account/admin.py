from django.contrib import admin

from account import models 


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'mobile', 'role', 'is_staff', 'is_superuser')


class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'medical_history', 'allergies', 'blood_type')


class VolunteerAdmin(admin.ModelAdmin):
    list_display = ('user', 'specialization', )


class NurseAdmin(admin.ModelAdmin):
    list_display = ('user', 'license_number', 'specialization', 'education')


class TeacherAdmin(admin.ModelAdmin):
    list_display = ('user', 'license_number', 'specialization', 'education')


admin.site.register(models.User, UserAdmin)
admin.site.register(models.StudentProfile, StudentAdmin)
admin.site.register(models.VolunteerProfile, VolunteerAdmin)
admin.site.register(models.NurseProfile, NurseAdmin)
admin.site.register(models.TeacherProfile, TeacherAdmin)