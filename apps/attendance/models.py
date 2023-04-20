from django.db import models
from apps.users.models import User

class Attendance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    is_present = models.BooleanField(default=False)


    def __str__(self):
        return self.user.user_name + str(self.date) + str(self.is_present)