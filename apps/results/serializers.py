from rest_framework import serializers
from .models import DeclareResult


class resultAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeclareResult
        fields = '__all__'




class resultListSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeclareResult
        fields = '__all__'
        depth=1