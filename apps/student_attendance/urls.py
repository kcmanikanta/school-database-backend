from django.urls import path
from .views import (
    StudentAttendanceList, 
    StudentAttendanceAdd, 
    StudentAttendanceStatsList,
    SchoolAttendanceStats,
    ClassAttendanceStats
)

urlpatterns = [
    path('list/', StudentAttendanceList.as_view(), name='student-attendance-list'),
    path('add/', StudentAttendanceAdd.as_view(), name='student-attendance-add'),
    path('stats/', StudentAttendanceStatsList.as_view(), name='student-attendance-stats'),
    path('school-stats/', SchoolAttendanceStats.as_view(), name='school-attendance-stats'),
    path('class-stats/<str:class_name>/', ClassAttendanceStats.as_view(), name='class-attendance-stats'),
]
