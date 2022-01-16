from django.test import TestCase
from ..models import School, Student
from django.contrib.gis.geos import GEOSGeometry

class SchoolTest(TestCase):
    """ Test module for School model """

    def setUp(self):
        School.objects.create(
            name='Manatal', max_student=5)
        School.objects.create(
            name='Depa', location=GEOSGeometry('POINT(100.55958059814 13.830890280799)', srid=4326))

    def test_school_distance(self):
        lat = 13.65769285185272
        lon = 100.66213835405992
        manatal = School.objects.get(name='Manatal')
        depa = School.objects.get(name='Depa')
        self.assertEqual(
            manatal.distance(lat, lon), None)
        self.assertLessEqual(
            depa.distance(lat, lon), 25)    # the distance should be about 22.22 km

class StudentTest(TestCase):
    """ Test module for Student model """

    def setUp(self):
        depa = School.objects.create(
            name='Depa', location=GEOSGeometry('POINT(100.55958059814 13.830890280799)', srid=4326))
        Student.objects.create(
            first_name='Wichai', last_name='Treethidtaphat', school=depa)         

    def test_student_id(self):
        wc = Student.objects.get(first_name='Wichai')
        self.assertLessEqual(len(wc.student_id), 20)
