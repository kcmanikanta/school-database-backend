from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('apps.users.urls')),
    path('attendance/', include('apps.attendance.urls')),
    path('admission/', include('apps.admission.urls')),
    path('student/', include('apps.students.urls')),
    path('result/', include('apps.results.urls')),
    path('subject/', include('apps.subjects.urls')),
    path('student-attendance/', include('apps.student_attendance.urls')),
    path('dob-record/', include('apps.dob_record.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
