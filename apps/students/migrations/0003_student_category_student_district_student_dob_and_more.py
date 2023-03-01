# Generated by Django 4.1.7 on 2023-02-16 19:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0002_student_photograph_student_signature'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='category',
            field=models.CharField(blank=True, default='ST', max_length=100, null=True, verbose_name='Category'),
        ),
        migrations.AddField(
            model_name='student',
            name='district',
            field=models.CharField(blank=True, default='Anantnag', max_length=100, null=True, verbose_name='District'),
        ),
        migrations.AddField(
            model_name='student',
            name='dob',
            field=models.DateField(blank=True, null=True, verbose_name='Date of Birth'),
        ),
        migrations.AddField(
            model_name='student',
            name='tehsil',
            field=models.CharField(blank=True, default='Srigufwara', max_length=100, null=True, verbose_name='Tehsil'),
        ),
        migrations.AddField(
            model_name='student',
            name='town',
            field=models.CharField(blank=True, default='Anantnag', max_length=100, null=True, verbose_name='Town'),
        ),
        migrations.AddField(
            model_name='student',
            name='udise_code',
            field=models.IntegerField(blank=True, null=True, verbose_name='UDISE_CODE'),
        ),
    ]