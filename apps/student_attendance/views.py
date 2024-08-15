from rest_framework import generics
from .models import StudentAttendance
from rest_framework.views import APIView
from .serializers import StudentAttendanceSerializer,StudentAttendanceStatsSerializer,SchoolAttendanceStatsSerializer, ClassAttendanceStatsSerializer
from django_filters import rest_framework as filters
from rest_framework import filters as search
from rest_framework.response import Response

# Filter for attendance records
class StudentAttendanceFilter(filters.FilterSet):
    class Meta:
        model = StudentAttendance
        fields = {
            'student__id': ['exact'],
            'student_class__class_name': ['exact'],
            'date': ['exact', 'gte', 'lte'],  
        }

# View to list attendance records
class StudentAttendanceList(generics.ListAPIView):
    queryset = StudentAttendance.objects.all()
    serializer_class = StudentAttendanceSerializer
    filter_backends = [filters.DjangoFilterBackend, search.SearchFilter]
    filterset_class = StudentAttendanceFilter
    search_fields = ['student__firstname', 'student__lastname', 'student__student_roll']

# View to add attendance records
class StudentAttendanceAdd(generics.CreateAPIView):
    queryset = StudentAttendance.objects.all()
    serializer_class = StudentAttendanceSerializer
    
class StudentAttendanceStatsList(generics.ListAPIView):
    serializer_class = StudentAttendanceStatsSerializer

    def get_queryset(self):
        student_id = self.request.query_params.get('student_id')
        if student_id:
            return StudentAttendance.objects.filter(student_id=student_id)
        return StudentAttendance.objects.none()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        student_id = self.request.query_params.get('student_id')
        if student_id:
            context['attendance'] = StudentAttendance.objects.filter(student_id=student_id)
        return context
    
    

# View for overall school attendance statistics
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import StudentAttendance, StudentClass
from .serializers import SchoolAttendanceStatsSerializer, ClassAttendanceStatsSerializer
from django.db import models
from django.db.models import Count, Q

class SchoolAttendanceStats(APIView):
    def get(self, request):
        # Aggregate attendance by class
        class_attendance = StudentAttendance.objects.values('student_class__class_name').annotate(
            total_present=Count('id', filter=Q(status='Present')),
            total_students=Count('student', distinct=True),
            total_days=Count('date', distinct=True)
        )
        
        total_school_days = StudentAttendance.objects.values('date').distinct().count()
        total_students = StudentAttendance.objects.values('student').distinct().count()
        overall_present = StudentAttendance.objects.filter(status='Present').count()
        
        data = []
        for cls in class_attendance:
            class_name = cls['student_class__class_name']
            class_present = cls['total_present']
            total_class_students = cls['total_students']
            class_days = cls['total_days']
            class_percentage = (class_present / (total_class_students * class_days)) * 100 if total_class_students * class_days > 0 else 0
            
            data.append({
                'class_name': class_name,
                'total_days_present': class_present,
                'total_days': class_days,
                'attendance_percentage': round(class_percentage, 2)
            })
        
        overall_percentage = (overall_present / (total_students * total_school_days)) * 100 if total_students * total_school_days > 0 else 0

        return Response({
            'classes': data,
            'overall_percentage': round(overall_percentage, 2)
        })


from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import StudentAttendance
from .serializers import ClassAttendanceStatsSerializer

class ClassAttendanceStats(APIView):
    def get(self, request, class_name):
        current_year = datetime.now().year
        current_month = datetime.now().month

        class_stats = StudentAttendance.objects.filter(
            student_class__class_name=class_name,
            date__year=current_year,
            date__month=current_month
        )
        
        total_days_present = class_stats.filter(status='Present').count()
        total_days_absent = class_stats.filter(status='Absent').count()
        total_days_leave = class_stats.filter(status='Leave').count()
        total_days = class_stats.values('date').distinct().count()
        total_students = class_stats.values('student').distinct().count()

        class_percentage = (total_days_present / (total_students * total_days)) * 100 if total_students * total_days > 0 else 0

        students = class_stats.values('student').distinct()
        student_data = []
        
        for student in students:
            student_id = student['student']
            student_attendance = class_stats.filter(student=student_id)
            student_present = student_attendance.filter(status='Present').count()
            student_total_days = student_attendance.values('date').distinct().count()
            student_percentage = (student_present / student_total_days) * 100 if student_total_days > 0 else 0

            student_info = StudentAttendance.objects.filter(student_id=student_id).first().student
            student_data.append({
                'id': student_id,
                'firstname': student_info.firstname,
                'lastname': student_info.lastname,
                'attendance_percentage': round(student_percentage, 2)
            })

        response_data = {
            'class_name': class_name,
            'total_days_present': total_days_present,
            'total_days_absent': total_days_absent,
            'total_days_leave': total_days_leave,
            'total_days': total_days,
            'attendance_percentage': round(class_percentage, 2),
            'students': student_data
        }
        
        return Response(response_data)
