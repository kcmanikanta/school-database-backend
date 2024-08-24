from rest_framework import serializers
from .models import PDFRecord
from apps.students.models import Student

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'firstname', 'lastname', 'student_roll']

class PDFRecordSerializer(serializers.ModelSerializer):
    student = StudentSerializer()
    class Meta:
        model = PDFRecord
        fields = ['id', 'student', 'image_url', 'created_at']
# In serializers.py

