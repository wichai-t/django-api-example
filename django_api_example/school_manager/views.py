from rest_framework import viewsets, permissions, filters
from .models import Student, School
from .serializers import SchoolSerializer, StudentSerializer


class StudentViewSet(viewsets.ModelViewSet):
    """
    ORM API viewset handling incoming requests, based on RESTful scheme.
    Support the "drf-nested-routers" to interact with student obj via a School routing.
    """
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = StudentSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['first_name', 'last_name', 'school__name']
    queryset = Student.objects.all()

    def get_queryset(self):
        qs = super(StudentViewSet, self).get_queryset()
        school_pk = self.kwargs.get('school_pk', None)
        if school_pk:
            return qs.filter(school=school_pk)
        else:
            return qs


class SchoolViewSet(viewsets.ModelViewSet):
    """
    Just a simple viewset showing the School models.
    Authentication is required to add or modify the model.
    """
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = SchoolSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    queryset = School.objects.all()
