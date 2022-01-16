from django.contrib import admin
from django.contrib.gis import admin as gis_admin
from .models import (School, Student)

class SchoolAdmin(gis_admin.GeoModelAdmin):
    """GeoModelAdmin to display and interact with location on a geo map"""

    list_display = ('name', 'num_of_student', 'max_student')
    search_fields = ('name',)

    # set default map zoom to Thailand
    default_lon = 101.22803
    default_lat = 13.60107
    default_zoom = 5

class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'first_name', 'last_name', 'get_school_name',)
    list_filter = ('school__name',)
    search_fields = ('first_name', 'last_name', 'school__name')

    @admin.display(description='School name')
    def get_school_name(self, obj):
        return obj.school.name

admin.site.register(School, SchoolAdmin)
admin.site.register(Student, StudentAdmin)
