from rest_framework import serializers
from .models import SubjectCombination, Subject, StudentClass

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ('subject_name', 'subject_code')

class StudentClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentClass
        fields = ('class_name',)

class SubjectCombinationSerializer(serializers.ModelSerializer):
    select_subject = SubjectSerializer()
    select_class = StudentClassSerializer()

    class Meta:
        model = SubjectCombination
        fields = ('select_subject', 'select_class')
