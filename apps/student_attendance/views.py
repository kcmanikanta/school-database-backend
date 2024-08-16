from rest_framework import generics
from .models import StudentAttendance
from rest_framework.views import APIView
from .serializers import StudentAttendanceSerializer,StudentAttendanceStatsSerializer
from django_filters import rest_framework as filters
from rest_framework import filters as search
from rest_framework.response import Response
from datetime import datetime
from django.db.models import Count, Q
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
    
from calendar import monthrange
from django.db.models import Count
from datetime import datetime
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response

class SchoolAttendanceStats(APIView):
    def get(self, request):
        view = request.query_params.get('view', 'monthly')  
        year = int(request.query_params.get('year', datetime.now().year))
        month = int(request.query_params.get('month', datetime.now().month))
        
        total_students_by_class = StudentAttendance.objects.values('student_class__class_name').annotate(
            total_students=Count('student', distinct=True)
        )

        if view == 'monthly':
            total_days_monthly = monthrange(year, month)[1]
            class_attendance_monthly = StudentAttendance.objects.filter(date__year=year, date__month=month).values('student_class__class_name').annotate(
                total_present=Count('id', filter=Q(status__in=['Present', 'Holiday'])),
                total_days=Count('date', distinct=True)
            )
            
            monthly_data = []
            for cls in class_attendance_monthly:
                class_name = cls['student_class__class_name']
                class_present = cls['total_present']
                total_students = next((item['total_students'] for item in total_students_by_class if item['student_class__class_name'] == class_name), 0)
                class_percentage = (class_present / (total_students * total_days_monthly)) * 100 if total_students * total_days_monthly > 0 else 0
                
                monthly_data.append({
                    'class_name': class_name,
                    'total_days_present': class_present,
                    'total_days': total_days_monthly,
                    'attendance_percentage': round(class_percentage, 2)
                })
            
            overall_present_monthly = sum(cls['total_days_present'] for cls in monthly_data)
            overall_percentage_monthly = (overall_present_monthly / (sum(item['total_students'] for item in total_students_by_class) * total_days_monthly)) * 100 if sum(item['total_students'] for item in total_students_by_class) * total_days_monthly > 0 else 0

            return Response({
                'monthly': {
                    'classes': monthly_data,
                    'overall_percentage': round(overall_percentage_monthly, 2)
                }
            })
        
        else:
            total_days_yearly = (datetime(year, 12, 31) - datetime(year, 1, 1)).days + 1
            class_attendance_yearly = StudentAttendance.objects.filter(date__year=year).values('student_class__class_name').annotate(
                total_present=Count('id', filter=Q(status__in=['Present', 'Holiday'])),
                total_days=Count('date', distinct=True)
            )
            
            yearly_data = []
            for cls in class_attendance_yearly:
                class_name = cls['student_class__class_name']
                class_present = cls['total_present']
                total_students = next((item['total_students'] for item in total_students_by_class if item['student_class__class_name'] == class_name), 0)
                class_percentage = (class_present / (total_students * total_days_yearly)) * 100 if total_students * total_days_yearly > 0 else 0
                
                yearly_data.append({
                    'class_name': class_name,
                    'total_days_present': class_present,
                    'total_days': total_days_yearly,
                    'attendance_percentage': round(class_percentage, 2)
                })
            
            overall_present_yearly = sum(cls['total_days_present'] for cls in yearly_data)
            overall_percentage_yearly = (overall_present_yearly / (sum(item['total_students'] for item in total_students_by_class) * total_days_yearly)) * 100 if sum(item['total_students'] for item in total_students_by_class) * total_days_yearly > 0 else 0

            return Response({
                'yearly': {
                    'classes': yearly_data,
                    'overall_percentage': round(overall_percentage_yearly, 2)
                }
            })




from datetime import datetime
from calendar import monthrange
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import StudentAttendance

class ClassAttendanceStats(APIView):
    def get(self, request, class_name):
        year = int(request.query_params.get('year', datetime.now().year))
        month = int(request.query_params.get('month', datetime.now().month))
        
        total_days_monthly = monthrange(year, month)[1]  # Total days in the specified month
        class_stats_monthly = StudentAttendance.objects.filter(
            student_class__class_name=class_name,
            date__year=year,
            date__month=month
        )

        total_days_present_monthly = class_stats_monthly.filter(status__in=['Present', 'Holiday']).count()
        total_days_absent_monthly = class_stats_monthly.filter(status='Absent').count()
        total_days_leave_monthly = class_stats_monthly.filter(status='Leave').count()

        class_percentage_monthly = (total_days_present_monthly / total_days_monthly) * 100 if total_days_monthly > 0 else 0

        total_days_yearly = (datetime(year, 12, 31) - datetime(year, 1, 1)).days + 1
        class_stats_yearly = StudentAttendance.objects.filter(
            student_class__class_name=class_name,
            date__year=year
        )
        
        total_days_present_yearly = class_stats_yearly.filter(status__in=['Present', 'Holiday']).count()
        total_days_absent_yearly = class_stats_yearly.filter(status='Absent').count()
        total_days_leave_yearly = class_stats_yearly.filter(status='Leave').count()

        class_percentage_yearly = (total_days_present_yearly / total_days_yearly) * 100 if total_days_yearly > 0 else 0

        students = class_stats_yearly.values('student').distinct()
        student_data = []
        
        for student in students:
            student_id = student['student']
            student_attendance_monthly = class_stats_monthly.filter(student=student_id)
            student_present_monthly = student_attendance_monthly.filter(status__in=['Present', 'Holiday']).count()
            
            student_attendance_yearly = class_stats_yearly.filter(student=student_id)
            student_present_yearly = student_attendance_yearly.filter(status__in=['Present', 'Holiday']).count()

            student_percentage_monthly = (student_present_monthly / total_days_monthly) * 100 if total_days_monthly > 0 else 0
            student_percentage_yearly = (student_present_yearly / total_days_yearly) * 100 if total_days_yearly > 0 else 0

            student_info = StudentAttendance.objects.filter(student_id=student_id).first().student
            student_data.append({
                'id': student_id,
                'firstname': student_info.firstname,
                'lastname': student_info.lastname,
                'attendance_percentage_monthly': round(student_percentage_monthly, 1),
                'attendance_percentage_yearly': round(student_percentage_yearly, 1)
            })

        response_data = {
            'class_name': class_name,
            'monthly': {
                'total_days_present': total_days_present_monthly,
                'total_days_absent': total_days_absent_monthly,
                'total_days_leave': total_days_leave_monthly,
                'total_days': total_days_monthly,
                'attendance_percentage': round(class_percentage_monthly, 1),
            },
            'yearly': {
                'total_days_present': total_days_present_yearly,
                'total_days_absent': total_days_absent_yearly,
                'total_days_leave': total_days_leave_yearly,
                'total_days': total_days_yearly,
                'attendance_percentage': round(class_percentage_yearly, 1),
            },
            'students': student_data
        }
        
        return Response(response_data)
