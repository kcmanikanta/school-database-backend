from rest_framework import serializers
from .models import DeclareResult, Subject, StudentClass

class DeclareResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeclareResult
        fields = ('id', 'select_student', 'subject', 'marks_obtained', 'total_marks')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['subject'] = instance.subject.subject_code
        return representation

class StudentMarksSerializer(serializers.Serializer):
    name = serializers.CharField()
    class_name = serializers.CharField(source='student_class.class_name')
    subjects = DeclareResultSerializer(many=True)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return {
            "name": data["name"],
            "class": data["class_name"],
            "subjects": [
                {
                    "subject": subject['subject'],
                    "marks_obtained": subject['marks_obtained'],
                    "total_marks": subject['total_marks']
                }
                for subject in data['subjects']
            ],
            "total_obtained": sum(subject['marks_obtained'] for subject in data['subjects']),
            "total_possible": sum(subject['total_marks'] for subject in data['subjects'])
        }

class ResultAddSerializer(serializers.ModelSerializer):
    subject_code = serializers.IntegerField(write_only=True)
    select_class_name = serializers.CharField(write_only=True)

    class Meta:
        model = DeclareResult
        fields = ('id', 'select_student', 'subject_code', 'select_class_name', 'marks_obtained', 'total_marks')

    def validate_subject_code(self, value):
        try:
            subject = Subject.objects.get(subject_code=value)
            return subject
        except Subject.DoesNotExist:
            raise serializers.ValidationError("Subject does not exist.")

    def validate_select_class_name(self, value):
        try:
            select_class = StudentClass.objects.get(class_name=value)
            return select_class
        except StudentClass.DoesNotExist:
            raise serializers.ValidationError("Class does not exist.")

    def create(self, validated_data):
        subject = validated_data.pop('subject_code')
        select_class = validated_data.pop('select_class_name')
        validated_data['subject'] = subject
        validated_data['select_class'] = select_class
        return DeclareResult.objects.create(**validated_data)
