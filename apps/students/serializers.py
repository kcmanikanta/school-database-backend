from rest_framework import serializers
from .models import Student
from apps.admission.models import Admission_form


class StudentAddSerializer(serializers.ModelSerializer):

    class Meta:
        model = Student
        fields = '__all__'
    def create(self, validated_data):
        admission = Admission_form.objects.get(email = validated_data['email'])
        admission.delete()
        print('firstName',validated_data['email'])


        return super().create(validated_data)
class StudentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'



