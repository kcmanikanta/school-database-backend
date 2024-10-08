from django.db import models
from cloudinary.models import CloudinaryField
from apps.student_classes.models import StudentClass
# from apps.results.models import DeclareResult
from apps.subjects.models import Subject

# Create your models here.
title = (
    ('Mr','Mr' ),
    ('Ms', 'Ms'),
    ('Mrs', 'Mrs')
)
gender = (
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Others', 'Others')
)

# Create your models here.
class Student(models.Model):
    class Meta:
     db_table = 'Students'
    student_roll = models.IntegerField(unique=True,blank=False,null=False)
    udise_code = models.CharField('UDISE_CODE', blank=True, null=True,max_length=50)
    title = models.CharField('title', max_length=20, choices=title)
    firstname = models.CharField('First Name',max_length=100,  db_index=True, blank=False, null = False )
    lastname = models.CharField('Last Name',max_length=100,  db_index=True, blank=False, null = False )
    email = models.EmailField('Email',max_length=500, blank=True, null=True)
    phone = models.BigIntegerField('Phone', blank=True, null=True)
    adhaar = models.BigIntegerField('Aadhar', blank=True, null=True)
    gender = models.CharField('Gender', max_length=50, blank=True, null=True, choices=gender)
    father = models.CharField('Father Name',max_length=100, db_index=True, blank=True, null = True )
    mother = models.CharField('Mother Name',max_length=100, db_index=True, blank=True, null = True )
    gaurdian = models.CharField('Gaurdian Name',max_length=100, db_index=True, blank=True, null = True )
    domicile = models.IntegerField('Domicile Number', blank = True, null = True)
    bank= models.CharField('Bank Account',null=True,blank=True,max_length=30)
    photograph = CloudinaryField(
        'Photo', blank = True, null = True
    )
    dob = models.DateField(
        'Date of Birth', blank=True, null=True
    )
    category = models.CharField(
        'Category', blank=True, null=True, default='ST',max_length=100
    )
    signature = CloudinaryField(
        'Signature', blank = True, null = True
    )
    town = models.CharField(
        'Town', blank=True, null=True, default='Anantnag' ,max_length=100
    )
    tehsil = models.CharField(
        'Tehsil', blank=True, null=True, default='Srigufwara',max_length=100
    )
    district = models.CharField(
        'District', blank=True, null=True, default='Anantnag',max_length=100
    )
    address = models.CharField(
        'Address', blank=True, null=True, default='Kasnard-Khiram',max_length=100
    )
    created_at = models.DateField('CreatedAt', blank = False,auto_now_add=True)
    updated_at = models.DateTimeField('UpdatedAt',auto_now=True , blank=True,null=True)
    student_class = models.ForeignKey(StudentClass, on_delete=models.CASCADE)
    def __str__(self):
        return self.firstname


    @property
    def student_details(self):
        self.related_student.all()

