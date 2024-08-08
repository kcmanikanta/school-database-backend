from django.db import models
from django.urls import reverse
from apps.student_classes.models import StudentClass


class Subject(models.Model):
    subject_name = models.CharField(max_length=100)
    subject_code = models.IntegerField(unique=True, primary_key=True)
    subject_creation_date = models.DateTimeField(auto_now=False, auto_now_add=True)
    subject_update_date = models.DateTimeField(auto_now=True, auto_now_add=False)

    class Meta:
        unique_together = ('subject_name', 'subject_code')

    def __str__(self):
        return self.subject_name

    def get_absolute_url(self):
        return reverse('subjects:subject_list')

    def results_marks(self):
        self.related_sub.all()


class SubjectCombination(models.Model):
    class Meta:
        unique_together = ('select_class','select_subject')
    select_class = models.ForeignKey(StudentClass, on_delete=models.CASCADE)
    select_subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    def get_absolute_url(self):
        return reverse('subjects:subject_combination_list')

    def __str__(self):
        return '%s Section-%s'%(self.select_class.class_name, self.select_class.section)
    
   