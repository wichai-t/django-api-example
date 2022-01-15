from django.contrib import admin
from .models import (School, Student)

class SchoolAdmin(admin.ModelAdmin):
    list_display = ('name', 'num_of_student', 'max_student')
    search_fields = ('name',)

class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'first_name', 'last_name', 'get_school_name',)
    list_filter = ('school__name',)
    search_fields = ('first_name', 'last_name', 'school__name')

    @admin.display(description='School name')
    def get_school_name(self, obj):
        return obj.school.name

admin.site.register(School, SchoolAdmin)
admin.site.register(Student, StudentAdmin)
