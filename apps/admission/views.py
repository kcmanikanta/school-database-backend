from django.shortcuts import render
from rest_framework import generics
from .models import Admission_form
from .serializers import AdmissionFormSerializer, AdmissionListSerializer
from apps.users.mixins import CustomLoginRequiredMixin
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend


from django_filters import rest_framework as filters

class AdmissionFormFilter(filters.FilterSet):
    id = filters.NumberFilter(field_name='id', lookup_expr='exact')

    class Meta:
        model = Admission_form
        fields = ['id', 'firstname', 'lastname']
# Create your views here.


class AdmissionFormView(generics.CreateAPIView):
    queryset = Admission_form.objects.all()
    serializer_class = AdmissionFormSerializer

    def create(self, request, *args, **kwargs,):
        return super().create(request, *args, **kwargs)



class AdmissionListView(generics.ListAPIView):
    queryset = Admission_form.objects.all()
    serializer_class = AdmissionListSerializer
    filter_backends = (DjangoFilterBackend, )
    filterset_class = AdmissionFormFilter
    search_fields = ['firstname', 'lastname']
    filterset_fields = ['id']


