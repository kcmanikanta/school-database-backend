from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from apps.students.models import Student
from .models import DeclareResult
from .serializers import ResultAddSerializer 
from rest_framework.exceptions import NotFound

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
            published = True  # Assume all results are published unless one is not

            for mark in marks:
                subject_marks.append({
                    "subject": mark.subject.subject_name,
                    "marks_obtained": mark.marks_obtained,
                    "total_marks": mark.total_marks
                })
                total_obtained += mark.marks_obtained if mark.marks_obtained is not None else 0
                total_possible += mark.total_marks if mark.total_marks is not None else 0

                # Update published status based on result's status
                if not mark.published:
                    published = False

            if subject_marks:
                data.append({
                    "id": student.id,
                    "name": student.firstname + ' ' + student.lastname,
                    "Admission No": student.student_roll,
                    "class": student.student_class.class_name,
                    "subjects": subject_marks,
                    "total_obtained": total_obtained,
                    "total_possible": total_possible,
                    "published": published  # Include published status
                })
        return Response(data, status=status.HTTP_200_OK)


class ResultView(APIView):
    def post(self, request):
        serializer = ResultAddSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Results added successfully."}, status=status.HTTP_201_CREATED)

    def put(self, request):
        serializer = ResultAddSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        updated_results = serializer.save() 
        
        
        result_data = ResultAddSerializer(updated_results, many=True).data
        return Response({"message": "Results updated successfully.", "results": result_data}, status=status.HTTP_200_OK)



class PublishResultView(APIView):
    def post(self, request):
        ids = request.data.get('ids', None)
        if ids:
            results = DeclareResult.objects.filter(id__in=ids)
        else:
            results = DeclareResult.objects.all()

        if not results.exists():
            return Response({"error": "No results found to publish."}, status=status.HTTP_404_NOT_FOUND)

        results.update(published=True)

        # Return the updated published status
        return Response({
            "message": "Results published successfully.",
            "published": True
        }, status=status.HTTP_200_OK)


class PublishedResultsView(APIView):
    def get(self, request):
        # Fetch only the results that have been published
        published_results = DeclareResult.objects.filter(published=True)

        if not published_results.exists():
            return Response({"error": "No published results found."}, status=status.HTTP_404_NOT_FOUND)

        # Serialize the results
        data = []
        for result in published_results:
            student = result.select_student
            data.append({
                "id": student.id,
                "name": student.firstname + ' ' + student.lastname,
                "Admission No": student.student_roll,
                "class": student.student_class.class_name,
                "subject": result.subject.subject_name,
                "marks_obtained": result.marks_obtained,
                "total_marks": result.total_marks,
                "published": result.published
            })
        
        return Response(data, status=status.HTTP_200_OK)

