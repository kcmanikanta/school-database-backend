from django.shortcuts import render
from .models import Student
from rest_framework import generics, status
from .serializers import StudentAddSerializer, StudentListSerializer
from django_filters import rest_framework as filters
from rest_framework import filters as search
from apps.users.mixins import CustomLoginRequiredMixin
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer

# Create your views here.

class StudentFilter(filters.FilterSet):
    class Meta:
        model = Student
        fields = {
            'id':['exact'],
            'student_roll':['exact'],
            'student_class':['exact']
        }

class StudentsAdd(generics.CreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentAddSerializer

    def post(self, request, *args, **kwargs):
        roll = request.data['student_roll']
        students = Student.objects.filter(student_roll = roll)
        if len(students) > 0:
            response = Response({'error': 'Student with Addmission No already exists' }, status=status.HTTP_400_BAD_REQUEST)
            response.accepted_renderer = JSONRenderer()
            response.accepted_media_type = "application/json"
            response.renderer_context = {}
            return response
        return self.create(request, *args, **kwargs)



class StudentsList(generics.ListAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentListSerializer
    filter_backends=[filters.DjangoFilterBackend,search.SearchFilter ]
    filterset_class = StudentFilter
    search_fields = ['firstname','lastname','udise_code','student_roll','father','mother']



class StudentUpdate(generics.UpdateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentListSerializer
    
    
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from .models import Student
from .serializers import StudentAddSerializer

class AdminStudentAddView(generics.CreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentAddSerializer

    def post(self, request, *args, **kwargs):
        # Check if the request data is a list (for multiple students)
        if isinstance(request.data, list):
            students = request.data
        else:
            students = [request.data]  # Make it a list if it's a single object

        created_students = []
        errors = []
        
        for student_data in students:
            roll = student_data.get('student_roll')
            if roll and Student.objects.filter(student_roll=roll).exists():
                errors.append({'student_roll': roll, 'error': 'Student with this Roll Number already exists'})
                continue

            serializer = self.get_serializer(data=student_data)
            if serializer.is_valid():
                serializer.save()
                created_students.append(serializer.data)
            else:
                errors.append({'student_roll': roll, 'error': serializer.errors})

        if errors:
            response_data = {'created': created_students, 'errors': errors}
            status_code = status.HTTP_400_BAD_REQUEST if len(errors) == len(students) else status.HTTP_207_MULTI_STATUS
        else:
            response_data = {'created': created_students}
            status_code = status.HTTP_201_CREATED

        response = Response(response_data, status=status_code)
        response.accepted_renderer = JSONRenderer()
        response.accepted_media_type = "application/json"
        response.renderer_context = {}
        return response

