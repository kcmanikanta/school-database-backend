from rest_framework import serializers
from .models import DeclareResult



class DeclareResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeclareResult
        fields = ('id', 'select_student', 'subject', 'marks')
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return {
            "subject": representation["subject"].subject_name,
            "marks": representation["marks"]
        }

class StudentMarksSerializer(serializers.Serializer):
    name = serializers.CharField()
    class_name = serializers.CharField(source='student_class.class_name')
    subjects = DeclareResultSerializer(many=True)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return {
            "name": data["name"],
            "class": data["class_name"],
            "subjects": {subject['subject']: subject['marks'] for subject in data['subjects']}
        }


class resultAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeclareResult
        fields = '__all__'




