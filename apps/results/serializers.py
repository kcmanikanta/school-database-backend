from rest_framework import serializers
from .models import DeclareResult


class resultAddSerializer(serializers.ModelSerializer):
    depth = 2
    class Meta:
        model = DeclareResult
        fields = '__all__'