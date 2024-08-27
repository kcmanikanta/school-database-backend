from rest_framework import serializers
from .models import TeacherProfile, Blog

class TeacherProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherProfile
        fields = ['id', 'name', 'expertise_subject', 'profile_picture']

class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ['id', 'teacher', 'subject', 'content', 'image', 'published', 'created_at']
