from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from faker import Faker
from ..models import School, Student
from ..serializers import SchoolSerializer, StudentSerializer

fake = Faker()

class GetAllObjsTest(APITestCase):
    """ Test module for GET all student and school APIs """

    def setUp(self):
        for _ in list(range(10)):
            sc = School.objects.create(name=fake.city())
            Student.objects.create(
                first_name=fake.first_name(), last_name=fake.last_name(), school=sc)

    def test_get_all_students(self):
        # get API response
        response = self.client.get('/students/?limit=20')
        # get data from db
        stds = Student.objects.all()
        serializer = StudentSerializer(stds, many=True)
        self.assertEqual(response.data['results'], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_get_all_schools(self):
        # get API response
        response = self.client.get('/schools/?limit=20')
        # get data from db
        scls = School.objects.all()
        serializer = SchoolSerializer(scls, many=True)
        self.assertEqual(response.data['results'], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class PostObjTest(APITestCase):
    """ Test module for POST create student and school APIs """

    def setUp(self):
        self.admin = User(username='admin', password='pass', is_staff=True)
        self.admin.save()

    def test_post_unauthorized(self):
        """ POST without authenticated should return HTTP 401 """

        response = self.client.post('/schools/', {'name': fake.city()}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_schools(self):
        """ POST with authorization should return HTTP 201 """

        self.client.force_authenticate(user=self.admin)
        statuses = []
        for _ in list(range(10)):
            response = self.client.post('/schools/', {'name': fake.city()}, format='json')
            statuses.append(response.status_code)

        # check if any POST is fail
        self.assertEqual(set(statuses), {status.HTTP_201_CREATED})

    def test_post_students(self):
        """ POST student with authorization should also return HTTP 201 """

        self.client.force_authenticate(user=self.admin)
        
        # create a school fisrt
        response = self.client.post('/schools/', {"name": fake.city()}, format='json')
        schl_id = response.data['id']
        statuses = []
        for _ in list(range(10)):
            response = self.client.post('/students/',
                {"school_id": schl_id,
                "first_name": fake.first_name(),
                "last_name": fake.last_name()}, format='json')
            statuses.append(response.status_code)
        # check if any POST is fail
        self.assertEqual(set(statuses), {status.HTTP_201_CREATED})

    def test_post_student_over_capacity(self):
        """ Create students more than school capacity should return error message """

        self.client.force_authenticate(user=self.admin)
        
        # create a school with student limit
        max_student = 5
        response = self.client.post('/schools/', {'name': fake.city(), 'max_student': max_student}, format='json')
        schl_id = response.data['id']
        pass_statuses = []
        for _ in list(range(10)):
            response = self.client.post('/students/',
                {"school_id": schl_id,
                "first_name": fake.first_name(),
                "last_name": fake.last_name()}, format='json')
            if response.status_code != 201:
                break
            pass_statuses.append(response.status_code)

        # the first max_student student creations should pass
        self.assertEqual(len(pass_statuses), max_student)
        self.assertEqual(set(pass_statuses), {status.HTTP_201_CREATED})
        # the 6th creation should fail
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)

class DeleteObjTest(APITestCase):
    """ Test module for DELETE student and school APIs """

    def setUp(self):
        # create an admin user and log in
        self.admin = User(username='admin', password='pass', is_staff=True)
        self.admin.save()
        self.client.force_authenticate(user=self.admin)

        # create 2 schools, with 10 students each
        for _ in list(range(2)):
            response = self.client.post('/schools/', {"name": fake.city()}, format='json')
            schl_id = response.data['id']
            for _ in list(range(10)):
                self.client.post('/students/',
                    {"school_id": schl_id,
                    "first_name": fake.first_name(),
                    "last_name": fake.last_name()}, format='json')

    def test_delete_school(self):
        """ DELETE a school should reduce its number """

        count_before = School.objects.count()
        scl_id = School.objects.last().id
        response = self.client.delete(f'/schools/{scl_id}/')

        # should return HTTP 204
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # the number should be lower by one
        self.assertEqual(School.objects.count(), count_before-1)

    def test_delete_student(self):
        """ DELETE a student should reduce its number """

        count_before = Student.objects.count()
        std_id = Student.objects.last().id
        response = self.client.delete(f'/students/{std_id}/')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # the number should be lower by one
        self.assertEqual(Student.objects.count(), count_before-1)
