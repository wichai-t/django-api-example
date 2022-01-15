"""URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path
from rest_framework import routers
from school_manager.views import StudentViewSet, SchoolViewSet

router = routers.SimpleRouter()
router.register(r'students', StudentViewSet)
router.register(r'schools', SchoolViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
]
urlpatterns += router.urls
