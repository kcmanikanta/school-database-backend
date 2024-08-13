from rest_framework import serializers
from .models import DeclareResult, Subject, StudentClass,Student

class DeclareResultSerializer(serializers.ModelSerializer):
    published = serializers.BooleanField()  # Include the published field

    class Meta:
        model = DeclareResult
        fields = ('id', 'select_student', 'subject', 'marks_obtained', 'total_marks', 'published')

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



class SubjectResultSerializer(serializers.ModelSerializer):
    subject_code = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = DeclareResult
        fields = ('subject_code', 'marks_obtained', 'total_marks')

    def validate_subject_code(self, value):
        try:
            subject = Subject.objects.get(subject_code=value)
            return subject
        except Subject.DoesNotExist:
            raise serializers.ValidationError("Subject does not exist.")

class ResultAddSerializer(serializers.Serializer):
    select_student = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all())
    select_class_name = serializers.CharField()
    results = SubjectResultSerializer(many=True)

    def validate_select_class_name(self, value):
        try:
            select_class = StudentClass.objects.get(class_name=value)
            return select_class
        except StudentClass.DoesNotExist:
            raise serializers.ValidationError("Class does not exist.")

    def create(self, validated_data):
        student = validated_data['select_student']
        select_class = validated_data['select_class_name']
        results_data = validated_data.pop('results')
        
        declare_results = []
        for result_data in results_data:
            subject = result_data.pop('subject_code')
            result_data['subject'] = subject
            result_data['select_class'] = select_class
            result_data['select_student'] = student
            declare_result, created = DeclareResult.objects.update_or_create(
                select_student=student,
                select_class=select_class,
                subject=subject,
                defaults=result_data
            )
            declare_results.append(declare_result)

        return declare_results

    def to_representation(self, instance):
        if isinstance(instance, list):
            return {
                "select_student": instance[0].select_student.id,
                "select_class_name": instance[0].select_class.class_name,
                "results": [
                    {
                        "subject_code": result.subject.subject_code,
                        "marks_obtained": result.marks_obtained,
                        "total_marks": result.total_marks
                    }
                    for result in instance
                ]
            }
        else:
            return {
                "select_student": instance.select_student.id,
                "select_class_name": instance.select_class.class_name,
                "results": [
                    {
                        "subject_code": instance.subject.subject_code,
                        "marks_obtained": instance.marks_obtained,
                        "total_marks": instance.total_marks
                    }
                ]
            }
