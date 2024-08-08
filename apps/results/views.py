from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from apps.students.models import Student
from .models import DeclareResult
from .serializers import ResultAddSerializer

class addResult(generics.CreateAPIView):
    queryset = DeclareResult.objects.all()
    serializer_class = ResultAddSerializer

class StudentMarksView(APIView):
    def get(self, request):
        students = Student.objects.all()

        # Filtering logic
        student_name = request.query_params.get('name', None)
        student_roll = request.query_params.get('roll', None)

        if student_name:
            students = students.filter(
                firstname__icontains=student_name) | students.filter(lastname__icontains=student_name)
        if student_roll:
            students = students.filter(student_roll=student_roll)

        data = []
        for student in students:
            marks = DeclareResult.objects.filter(select_student=student)
            subject_marks = []
            total_obtained = 0
            total_possible = 0
            for mark in marks:
                subject_marks.append({
                    "subject": mark.subject.subject_name,
                    "marks_obtained": mark.marks_obtained,
                    "total_marks": mark.total_marks
                })
                total_obtained += mark.marks_obtained if mark.marks_obtained is not None else 0
                total_possible += mark.total_marks if mark.total_marks is not None else 0

            if subject_marks:
                data.append({
                    "name": student.firstname + ' ' + student.lastname,
                    "Admission No": student.student_roll,
                    "class": student.student_class.class_name,
                    "subjects": subject_marks,
                    "total_obtained": total_obtained,
                    "total_possible": total_possible
                })
        return Response(data, status=status.HTTP_200_OK)
