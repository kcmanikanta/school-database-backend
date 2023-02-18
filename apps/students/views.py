from django.shortcuts import render
from .models import Student
from rest_framework import generics
from .serializers import StudentAddSerializer, StudentListSerializer
from django_filters import rest_framework as filters
from rest_framework import filters as search
from apps.users.mixins import CustomLoginRequiredMixin

# Create your views here.

# class StudentFilter(filters.FilterSet):
#     class Meta:
#         model = Student
#         fields = {
#             'id':['exact']
#         }


class StudentsAdd(generics.CreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentAddSerializer



class StudentsList(generics.ListAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentListSerializer
    filter_backends=[filters.DjangoFilterBackend,search.SearchFilter ]
    filterset_fields = ['id','student_roll','student_class']
    search_fields = ['firstname','lastname','udise_code','student_roll']



