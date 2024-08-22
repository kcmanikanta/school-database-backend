from rest_framework import serializers
from .models import Admission_form

from rest_framework import serializers
from .models import Admission_form

class AdmissionFormSerializer(serializers.ModelSerializer):
    signature = serializers.ImageField(required=False)
    photograph = serializers.ImageField(required=False)

    class Meta:
        model = Admission_form
        fields = '__all__'

    def create(self, validated_data):
        # Extract the files from validated data
        photograph = validated_data.pop('photograph', None)
        signature = validated_data.pop('signature', None)

        # Create the Admission_form object
        admission_form = Admission_form.objects.create(**validated_data)

        # If a photograph is provided, save it
        if photograph:
            admission_form.photograph = photograph
            admission_form.save()

        # If a signature is provided, save it
        if signature:
            admission_form.signature = signature
            admission_form.save()

        return admission_form



class AdmissionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admission_form
        fields= '__all__'