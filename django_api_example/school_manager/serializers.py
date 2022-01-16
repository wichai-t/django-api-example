from rest_framework import serializers
from rest_framework.exceptions import NotAcceptable
from .exceptions import TooManyStudentError
from .models import Student, School


class SchoolSerializer(serializers.ModelSerializer):

    class Meta:
        model = School
        exclude = ()

class StudentSerializer(serializers.ModelSerializer):

    school = SchoolSerializer(read_only=True)

    # The below field is used to write related school back to a new student obj
    # but not showing up in the response.
    school_id = serializers.PrimaryKeyRelatedField(
        queryset=School.objects.all(), source='school', write_only=True)

    class Meta:
        model = Student
        exclude = ()

    def create(self, validated_data):
        try:
            return super(StudentSerializer, self).create(validated_data)
        except TooManyStudentError as e:
            raise NotAcceptable(str(e))
        except Exception as e:
            # handle other exceptions here.
            raise e