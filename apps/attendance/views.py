from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from .serializers import AttendanceSerializer, AttendanceReportSerializer
from apps.users.mixins import CustomLoginRequiredMixin
from .models import Attendance
from django_filters import rest_framework as filters
from rest_framework import filters as search


# Create your views here.
class AttendanceView(CustomLoginRequiredMixin, generics.CreateAPIView):
    serializer_class = AttendanceSerializer

    def create(self, request, *args, **kwargs):
        data = request.data.copy()  # create a mutable copy of the request data
        data["user"] = request.login_user.id  # set the user field to the user ID
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


    def create(self, request, *args, **kwargs):
        data = request.data.copy()  # create a mutable copy of the request data
        data["user"] = request.login_user.id  # set the user field to the user ID
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class AttendnaceFilter(filters.FilterSet):
    class Meta:
        model = Attendance
        fields = {
            'user':['exact'],
        }


class AttendanceReportView(CustomLoginRequiredMixin, generics.ListAPIView):
    
    serializer_class = AttendanceReportSerializer
    queryset = Attendance.objects.all()
    filter_backends=[filters.DjangoFilterBackend,search.SearchFilter ]
    filterset_class = AttendnaceFilter
    search_fields = ['user','email']

    def get(self, request, *args, **kwrgs):
        queryset = self.get_queryset().filter(user=request.login_user.id)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)



class AttendanceAdminView(generics.ListAPIView):
    
    serializer_class = AttendanceReportSerializer
    queryset = Attendance.objects.all()
    filter_backends=[filters.DjangoFilterBackend,search.SearchFilter ]
    filterset_class = AttendnaceFilter