from django.db import models
from apps.students.models import Student

class PDFRecord(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    image_url = models.URLField(blank=True, null=True) 
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.firstname} {self.student.lastname} - PDF Record"
