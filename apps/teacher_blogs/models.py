from django.db import models
from cloudinary.models import CloudinaryField

class TeacherProfile(models.Model):
    name = models.CharField(max_length=100)
    expertise_subject = models.CharField(max_length=100)
    profile_picture = CloudinaryField('image', blank=True, null=True)

    def __str__(self):
        return self.name

class Blog(models.Model):
    teacher = models.ForeignKey(TeacherProfile, on_delete=models.CASCADE, related_name='blogs')
    subject = models.CharField(max_length=150)
    content = models.TextField()
    image = CloudinaryField('image', blank=False, null=False)
    published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.teacher.name} - {self.subject}"
