from django.db import models
from django.contrib.gis.db.models import PointField
import uuid
from .exceptions import TooManyStudentError

def id_generator(length=6):
    """ A simple unique ID generator for the Student model"""
    while True:
        code = uuid.uuid4().hex[:length].upper()
        if not Student.objects.filter(student_id=code).exists():
            return code

class Student(models.Model):
    """ Student model
    - Students have a first name, a last name, and a student identification string (20 characters max for each)
    - Each student object must belong to a school object (Many-to-one relationships)
    - The student id is automatically generated as 6 HEX number to easily remembered and enough for a school
    - Has education level as a choice
    """
    LEVEL_CHOICES = [
        ('PRE', 'Preschool'),
        ('ELE', 'Elementary'),
        ('MID', 'Middle'),
        ('HIG', 'High'),
        ('OTH', 'Other'),
    ]
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    # for 6 hexes, a school can have more than 16M unique student ids
    student_id = models.CharField(default=id_generator, editable=False, unique=True, max_length=20)
    school = models.ForeignKey('School', on_delete=models.CASCADE)
    level = models.CharField(max_length=3, choices=LEVEL_CHOICES, default='OTH', verbose_name='Education Level') 

    def __str__(self):
        return '%s: %s' % (self.student_id, self.full_name)

    @property
    def full_name(self):
        "Returns the student's full name."
        return '%s %s' % (self.first_name, self.last_name)

    def save(self, *args, **kwargs):
        school_max_student = self.school.max_student
        if self.school.student_set.count() < school_max_student:
            super(Student, self).save()
        else:
            raise TooManyStudentError(self.school.name, school_max_student)

class School(models.Model):
    """ Schools have a name (20 char max) and a maximum number of student (any positive integer)
    """
    name = models.CharField(max_length=20)
    max_student = models.IntegerField(verbose_name='Maximum number of student', default=3000)
    location = PointField(blank=True, null=True)    # a geo field

    def __str__(self):
        return '%s: %s' % (self.id, self.name)

    @property
    def num_of_student(self):
        "Returns the current number of student."
        return self.student_set.count()

    def distance(self, lat, lon):
        """ An utility fn to calculate distance between the given lat, lon position and the school location.

        Args:
            lat (float): The query latitude.
            lon (float): The query longitude.

        Returns:
            Caculated distance in km. A float if location is available, None otherwise.
        """
        if not self.location:
            return None
        from django.contrib.gis.db.models.functions import Distance
        from django.contrib.gis.geos import GEOSGeometry

        pnt = GEOSGeometry('POINT(%s %s)' % (lon, lat), srid=4326)        
        qs = School.objects.filter(pk=self.pk)
        return qs.annotate(distance=Distance('location', pnt))[0].distance.m/1000
