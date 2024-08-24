from rest_framework import serializers
from .models import PDFRecord
from apps.students.models import Student

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'firstname', 'lastname', 'student_roll']

class PDFRecordSerializer(serializers.ModelSerializer):
    student = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all())

    class Meta:
        model = PDFRecord
        fields = ['id', 'student', 'image_url', 'created_at']

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['student'] = StudentSerializer(instance.student).data
        return ret
