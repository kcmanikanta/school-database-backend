from rest_framework import serializers
from .models import StudentAttendance
from apps.students.models import Student

class StudentAttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentAttendance
        fields = '__all__'
        

from rest_framework import serializers
from .models import StudentAttendance

class StudentAttendanceRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentAttendance
        fields = ['date', 'status']

class StudentAttendanceStatsSerializer(serializers.ModelSerializer):
    total_days_present = serializers.SerializerMethodField()
    total_days_absent = serializers.SerializerMethodField()
    total_days_leave = serializers.SerializerMethodField()
    total_days = serializers.SerializerMethodField()
    attendance_percentage = serializers.SerializerMethodField()
    student = serializers.SerializerMethodField()
    attendance_records = serializers.SerializerMethodField()

    class Meta:
        model = StudentAttendance
        fields = [
            'student', 
            'total_days_present', 
            'total_days_absent', 
            'total_days_leave', 
            'total_days', 
            'attendance_percentage',
            'attendance_records',
        ]

    def get_total_days_present(self, obj):
        return self.context['attendance'].filter(status='Present').count()

    def get_total_days_absent(self, obj):
        return self.context['attendance'].filter(status='Absent').count()

    def get_total_days_leave(self, obj):
        return self.context['attendance'].filter(status='Leave').count()

    def get_total_days(self, obj):
        return self.context['attendance'].count()

    def get_attendance_percentage(self, obj):
        total_days = self.get_total_days(obj)
        total_days_present = self.get_total_days_present(obj)
        if total_days > 0:
            percentage = (total_days_present / total_days) * 100
            return round(percentage, 2)
        return 0

    def get_student(self, obj):
        return {
            "firstname": obj.student.firstname,
            "lastname": obj.student.lastname,
        }

    def get_attendance_records(self, obj):
        return StudentAttendanceRecordSerializer(self.context['attendance'], many=True).data
    



class SchoolAttendanceStatsSerializer(serializers.Serializer):
    class_name = serializers.CharField()
    total_days_present = serializers.IntegerField()
    total_days = serializers.IntegerField()
    attendance_percentage = serializers.FloatField()

class SchoolOverallStatsSerializer(serializers.Serializer):
    classes = SchoolAttendanceStatsSerializer(many=True)
    overall_percentage = serializers.FloatField()


from rest_framework import serializers
from apps.students.models import Student


class StudentSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    firstname = serializers.CharField()
    lastname = serializers.CharField()
    attendance_percentage = serializers.FloatField()

class ClassAttendanceStatsSerializer(serializers.Serializer):
    class_name = serializers.CharField()
    total_days_present = serializers.IntegerField()
    total_days_absent = serializers.IntegerField()
    total_days_leave = serializers.IntegerField()
    total_days = serializers.IntegerField()
    attendance_percentage = serializers.FloatField()
    students = serializers.ListSerializer(child=StudentSerializer(), allow_empty=True)


