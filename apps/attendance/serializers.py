from .models import Attendance
from rest_framework import serializers

class AttendanceSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.user_name', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = Attendance
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        image = request.FILES.get('photo')
        attendance = Attendance.objects.create(
            user=validated_data['user'],
            status=validated_data['status'],
            location=validated_data['location'],
            imageUrl=image
        )
        return attendance

class AttendanceReportSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.user_name', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = Attendance
        fields = '__all__'
