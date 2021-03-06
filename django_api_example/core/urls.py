"""URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
"""
from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework_nested import routers
from school_manager.views import StudentViewSet, SchoolViewSet, index

router = routers.SimpleRouter()
router.register(r'students', StudentViewSet)
router.register(r'schools', SchoolViewSet)

schools_router = routers.NestedSimpleRouter(router, r'schools', lookup='school')
schools_router.register(r'students', StudentViewSet, basename='school-students')

urlpatterns = [
    path('', index, name='index'),
    path(f'{settings.ADMIN_URL}', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api-token-auth/', obtain_jwt_token),
    path(r'', include(router.urls)),
    path(r'', include(schools_router.urls)),
]
