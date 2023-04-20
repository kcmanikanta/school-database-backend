from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from .serializers import AttendanceSerializer
from apps.users.mixins import CustomLoginRequiredMixin


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


