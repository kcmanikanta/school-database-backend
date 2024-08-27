from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TeacherProfileViewSet, BlogViewSet

router = DefaultRouter()
router.register(r'teachers', TeacherProfileViewSet)
router.register(r'blogs', BlogViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
