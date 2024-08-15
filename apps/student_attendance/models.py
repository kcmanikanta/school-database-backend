from datetime import datetime
from django.db import models
from apps.students.models import Student
from apps.student_classes.models import StudentClass

attendance_status = (
    ('Present', 'Present'),
    ('Absent', 'Absent'),
    ('Leave', 'Leave')
)

class StudentAttendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="attendance")
    student_class = models.ForeignKey(StudentClass, on_delete=models.CASCADE)
    date = models.DateField('Date', blank=False, null=False)
    status = models.CharField('Status', max_length=20, choices=attendance_status, default='Present')
    remarks = models.TextField('Remarks', blank=True, null=True)

    class Meta:
        unique_together = (('student', 'date'),)  
        db_table = 'StudentAttendance'

    def __str__(self):
        return f"{self.student.firstname} {self.student.lastname} - {self.date} - {self.status}"

    def get_session_dates(self):
        current_year = datetime.now().year
        start_date = datetime(current_year, 3, 1).date()
        end_date = datetime(current_year + 1, 3, 31).date()
        return start_date, end_date

    def total_days_present(self):
        start_date, end_date = self.get_session_dates()
        return self.__class__.objects.filter(student=self.student, status='Present', date__range=[start_date, end_date]).count()

    def total_days_absent(self):
        start_date, end_date = self.get_session_dates()
        return self.__class__.objects.filter(student=self.student, status='Absent', date__range=[start_date, end_date]).count()

    def total_days_leave(self):
        start_date, end_date = self.get_session_dates()
        return self.__class__.objects.filter(student=self.student, status='Leave', date__range=[start_date, end_date]).count()

    def total_days(self):
        start_date, end_date = self.get_session_dates()
        # Count the number of distinct days where attendance is recorded for this student within the session dates
        total_days = self.__class__.objects.filter(student=self.student, date__range=[start_date, end_date]).values('date').distinct().count()
        return total_days

    def attendance_percentage(self):
        total_days = self.total_days()
        present_days = self.total_days_present()
        if total_days > 0:
            percentage = (present_days / total_days) * 100
            return round(percentage, 2)  # Rounds to 2 decimal places
        return 0

    def attendance_summary(self):
        return {
            'total_days_present': self.total_days_present(),
            'total_days_absent': self.total_days_absent(),
            'total_days_leave': self.total_days_leave(),
            'total_days': self.total_days(),
            'attendance_percentage': self.attendance_percentage()
        }
