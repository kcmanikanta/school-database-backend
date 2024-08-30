from django.db import models
from apps.subjects.models import StudentClass, Subject
from apps.students.models import Student

class DeclareResult(models.Model):
    select_class = models.ForeignKey(StudentClass, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    select_student = models.ForeignKey(Student, on_delete=models.CASCADE)
    marks_obtained = models.IntegerField('Marks Obtained', db_index=True, blank=True, null=True)
    total_marks = models.IntegerField('Total Marks', blank=True, null=True)
    published = models.BooleanField(default=False)
    year = models.IntegerField('Year')

    class Meta:
        unique_together = (('select_student', 'subject', 'select_class', 'year'),)

    def __str__(self):
        return "%s Section-%s Year-%d" % (self.select_class.class_name, self.select_class.section, self.year)

    def save(self, *args, **kwargs):
        # Save the result first before promoting the student
        super().save(*args, **kwargs)

        # Handle promotion after saving the result
        if self.marks_obtained and self.total_marks:
            percentage = (self.marks_obtained / self.total_marks) * 100
            if percentage >= 33:
                self.promote_student()

    def promote_student(self):
        next_class = self.select_class.get_next_class()
        if next_class:
            # This will update the student's class without altering the declared result's class.
            self.select_student.student_class = next_class
            self.select_student.save()
