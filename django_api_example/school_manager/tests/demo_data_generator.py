from random import randint, uniform
from faker import Faker
from django.contrib.gis.geos import GEOSGeometry
from ..models import School, Student

fake = Faker()

def demo_data_generator(num_school, num_student=[5, 20], lat=None, lon=None):
    """ Randomly generate demo data.

    Args:
        num_school (int):                   Number of schools to generate.
        num_student (int | list, optional): Number of students in each school to generate.
                                            Use list of [MIN, MAX] to random value between them.
        lat (float | list, optional):       The school location latitude.
                                            Use list of [MIN, MAX] to random value between them.
        lon (float | list, optional):       The school location longitude.
                                            Use list of [MIN, MAX] to random value between them.

    Returns: None

    Examples:
        Example function calling.
            >>> demo_data_generator(
                10, lat=[19.38858112920021, 13.225030865369293],
                lon=[97.87590502012021, 104.4789620482098])

    """
    for i in range(num_school):

        # if any input is list of min and max values, we will random value between them
        _num_student = randint(*num_student) if isinstance(num_student, list) else num_student
        if None in (lat, lon):
            # undefine location
            sc = School.objects.create(name=fake.city())
        else:
            _lat = uniform(*lat) if isinstance(lat, list) else lat
            _lon = uniform(*lon) if isinstance(lon, list) else lon
            sc = School.objects.create(
                name=fake.city(),
                location=GEOSGeometry(f'POINT({_lat} {_lon})', srid=4326)
            )

        # add students to the school
        for j in range(_num_student):
            Student.objects.create(
                first_name=fake.first_name(), last_name=fake.last_name(), school=sc
            )
