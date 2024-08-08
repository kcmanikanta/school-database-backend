from django.db import models
from apps.users.models import User
from cloudinary.models import CloudinaryField

statuses = (
    ('present', 'present'),
    ('absent', "absent"),
    ('leave', 'leave'),
    ('duty', 'duty'),
    ('Present', 'Present'),
    ('Absent', "Absent"),
    ('Leave', 'Leave'),
    ('Duty', 'Duty')
)

class Attendance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    imageUrl = CloudinaryField(blank=True, null=True)
    create_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(default="absent", blank=False, null=False, max_length=50, choices=statuses)
    location = models.CharField(blank=True, null=True, max_length=300)

    def __str__(self):
        return self.user.user_name + str(self.date) + self.status
