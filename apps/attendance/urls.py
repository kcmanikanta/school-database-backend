from django.urls import path
from .views import AttendanceView,AttendanceReportView

urlpatterns = [
    path('add/', AttendanceView.as_view(), name='attendance'),
    path('report/', AttendanceReportView.as_view(), name='attendance-report'),
]
