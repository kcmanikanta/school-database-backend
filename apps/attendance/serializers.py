from .models import Attendance
from rest_framework import serializers

class AttendanceSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.user_name', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = Attendance
        fields = '__all__'
