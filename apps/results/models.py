from django.db import models
from apps.subjects.models import StudentClass, Subject
from apps.students.models import Student

class DeclareResult(models.Model):
    select_class = models.ForeignKey(StudentClass, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    select_student = models.ForeignKey(Student, on_delete=models.CASCADE)
    marks_obtained = models.IntegerField('Marks Obtained', db_index=True, blank=True, null=True)
    total_marks = models.IntegerField('Total Marks', blank=True, null=True)  # New field

    class Meta:
        unique_together = (('select_student', 'subject', 'select_class'),)

    def __str__(self):
        return "%s Section-%s" % (self.select_class.class_name, self.select_class.section)
