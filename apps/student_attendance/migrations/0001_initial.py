# Generated by Django 5.0.3 on 2024-08-14 19:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('student_classes', '0001_initial'),
        ('students', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentAttendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='Date')),
                ('status', models.CharField(choices=[('Present', 'Present'), ('Absent', 'Absent'), ('Leave', 'Leave')], default='Present', max_length=20, verbose_name='Status')),
                ('remarks', models.TextField(blank=True, null=True, verbose_name='Remarks')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attendance', to='students.student')),
                ('student_class', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student_classes.studentclass')),
            ],
            options={
                'db_table': 'StudentAttendance',
                'unique_together': {('student', 'date')},
            },
        ),
    ]