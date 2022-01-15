from rest_framework import serializers
from .models import Student, School


class StudentSerializer(serializers.ModelSerializer):

    school_name = serializers.SerializerMethodField()

    class Meta:
        model = Student
        exclude = ()
        # fields = ['first_name']

    def get_school_name(self, obj):
        return obj.school.name

class SchoolSerializer(serializers.ModelSerializer):

    class Meta:
        model = School
        exclude = ()
