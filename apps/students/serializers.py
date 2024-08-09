from rest_framework import serializers
from .models import Student
from apps.admission.models import Admission_form


class StudentAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'
    
    def create(self, validated_data):
        email = validated_data.get('email')
        if email:
            try:
                # Attempt to find and delete the admission form if it exists
                admission = Admission_form.objects.get(email=email)
                admission.delete()
                print('Deleted admission form for email:', email)
            except Admission_form.DoesNotExist:
                # Log a message or handle the case where the admission form does not exist
                print('No admission form found for email:', email)
        
        return super().create(validated_data)
class StudentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'



