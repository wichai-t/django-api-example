from django.contrib.auth.models import User, Group
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Student, School
from .serializers import SchoolSerializer, StudentSerializer


class StudentViewSet(viewsets.ModelViewSet):
    """
    ...
    """
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    # renderer_classes = (renderers.JSONRenderer, renderers.TemplateHTMLRenderer)
    serializer_class = StudentSerializer
    queryset = Student.objects.all()

    def list(self, request, *args, **kwargs):
        qs = self.get_queryset()
        page = self.paginate_queryset(qs)
        serialized = self.get_serializer(page, many=True)
        return Response(serialized.data)

    def retrieve(self, request, pk=None):
        qs = self.get_queryset()
        std = get_object_or_404(qs, pk=pk)
        serializer = self.get_serializer(std)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        # TODO if any
        return super(StudentViewSet, self).create(request, *args, **kwargs)

class SchoolViewSet(viewsets.ModelViewSet):
    """
    ...
    """
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = SchoolSerializer
    queryset = School.objects.all()

    def list(self, request, *args, **kwargs):
        qs = self.get_queryset()
        page = self.paginate_queryset(qs)
        serialized = self.get_serializer(page, many=True)
        return Response(serialized.data)

    def retrieve(self, request, pk=None):
        qs = self.get_queryset()
        scl = get_object_or_404(qs, pk=pk)
        serializer = self.get_serializer(scl)
        return Response(serializer.data)