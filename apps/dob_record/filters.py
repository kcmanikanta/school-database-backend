# In filters.py

import django_filters
from .models import PDFRecord

class PDFRecordFilter(django_filters.FilterSet):
    student_roll = django_filters.CharFilter(field_name='student__student_roll', lookup_expr='icontains')
    firstname = django_filters.CharFilter(field_name='student__firstname', lookup_expr='icontains')
    lastname = django_filters.CharFilter(field_name='student__lastname', lookup_expr='icontains')

    class Meta:
        model = PDFRecord
        fields = ['student_roll', 'firstname', 'lastname']
