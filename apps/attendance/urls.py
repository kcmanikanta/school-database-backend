from django.urls import path
from .views import AttendanceView

urlpatterns = [
    path('add/', AttendanceView.as_view(), name='attendance'),
]
