from django.urls import path
from .views import AttendanceView,AttendanceReportView,AttendanceAdminView

urlpatterns = [
    path('add/', AttendanceView.as_view(), name='attendance'),
    path('report/', AttendanceReportView.as_view(), name='attendance-report'),
    path('adminreport',AttendanceAdminView.as_view(),name='admin-attendance-view')
]
