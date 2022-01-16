from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from faker import Faker
from ..models import School, Student
from ..serializers import StudentSerializer

fake = Faker()

class NestedRouterTest(APITestCase):
    """ Test module for nested routers, which will check these:
    - Endpoint /schools/:id/students will return students who belong to school :id (GET)
    - Endpoint /schools/:id/students will allow student creation in the school :id (POST)
    - Endpoint will allow GET/PUT/PATCH/DELETE methods on /schools/:id/students/:id
    - Endpoint will respect the two rules
        1. generate a unique identification string for a student
        2. if exceed maximum number of student, it will return a DRF error message
    """

    def setUp(self):
        # create an admin user and log in
        self.admin = User(username='admin', password='pass', is_staff=True)
        self.admin.save()
        self.client.force_authenticate(user=self.admin)

        # Foo school has 10 students, and maximum is 15
        self.foo_max = 15
        sc = School.objects.create(name='Foo', max_student=self.foo_max)
        for _ in list(range(10)):
            Student.objects.create(
                first_name=fake.first_name(), last_name=fake.last_name(), school=sc)

        # Bar school has 5 students
        sc = School.objects.create(name='Bar')
        for _ in list(range(5)):
            Student.objects.create(
                first_name=fake.first_name(), last_name=fake.last_name(), school=sc)

    def test_get_foo_students(self):
        """ The Foo must have 10 students """
        foo_id = School.objects.get(name='Foo').id
        response = self.client.get(f'/schools/{foo_id}/students/?limit=20')
        self.assertEqual(response.data['count'], 10)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_foo_student(self):
        """ Using POST to create a new Foo's student.
        Foo must have 11 students now.
        """
        foo_id = School.objects.get(name='Foo').id
        response = self.client.post(f'/schools/{foo_id}/students/',
                {"school_id": foo_id,
                "first_name": fake.first_name(),
                "last_name": fake.last_name()}, format='json')

        # check if the status is correct
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Foo must have 11 students now.
        response = self.client.get(f'/schools/{foo_id}/students/?limit=20')
        self.assertEqual(response.data['count'], 11)

    def test_foo_student_item(self):
        """ Test if endpoint allow GET/PUT/PATCH/DELETE methods on /schools/:id/students/:id
        """
        foo = School.objects.get(name='Foo')
        std = foo.student_set.first()

        # check if GET response is the same as from db
        response = self.client.get(f'/schools/{foo.id}/students/{std.id}/')
        serializer = StudentSerializer(std)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # check if PATCH response is OK
        response = self.client.patch(f'/schools/{foo.id}/students/{std.id}/',
                    {"last_name": fake.last_name()}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # check if DELETE response is correct
        response = self.client.delete(f'/schools/{foo.id}/students/{std.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # Foo must have 9 students now.
        response = self.client.get(f'/schools/{foo.id}/students/?limit=20')
        self.assertEqual(response.data['count'], 9)

    def test_post_student_over_capacity(self):
        """ Create students more than Foo capacity should return error message """        
        foo = School.objects.get(name='Foo')

        for _ in list(range(10)):
            response = self.client.post(f'/schools/{foo.id}/students/',
                {"school_id": foo.id,
                "first_name": fake.first_name(),
                "last_name": fake.last_name()}, format='json')
            if response.status_code != 201:
                err_code = response.status_code

        # now Foo should have its max student
        response = self.client.get(f'/schools/{foo.id}/students/?limit=20')
        self.assertEqual(response.data['count'], self.foo_max)
        # the over student creation should fail
        self.assertEqual(err_code, status.HTTP_406_NOT_ACCEPTABLE)
