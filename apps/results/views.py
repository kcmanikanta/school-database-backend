from rest_framework import generics, status
from .models import DeclareResult
from .serializers import resultAddSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from apps.students.models import Student


class StudentMarksView(APIView):
    
    def get(self, request):
        students = Student.objects.all()
        data = []
        for student in students:
            marks = DeclareResult.objects.filter(select_student=student)
            subject_marks = {}
            for mark in marks:
                subject_marks[mark.subject.subject_name] = mark.marks
            if  subject_marks != {} :
                data.append({
                    "name": student.firstname + ' '+student.lastname,
                    "Admission No": student.student_roll,
                    "class": student.student_class.class_name,
                    "subjects": subject_marks
                })
        return Response(data, status=status.HTTP_200_OK)




class addResult(generics.CreateAPIView):
    queryset = DeclareResult.objects.all()
    serializer_class = resultAddSerializer