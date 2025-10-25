from django.contrib import admin

from account import models 


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'mobile', 'get_full_name', 'role', 'is_staff', 'is_superuser')


class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'consecutive_login_days', 'school_name', 'grade', 'last_year_avg')


class TeacherAdmin(admin.ModelAdmin):
    list_display = ('user', 'license_number', 'specialization', 'education')


admin.site.register(models.User, UserAdmin)
admin.site.register(models.StudentProfile, StudentAdmin)
admin.site.register(models.TeacherProfile, TeacherAdmin)