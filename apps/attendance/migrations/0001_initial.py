# Generated by Django 5.0.3 on 2024-08-14 20:22

import cloudinary.models
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('imageUrl', cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('present', 'present'), ('absent', 'absent'), ('leave', 'leave'), ('duty', 'duty'), ('Present', 'Present'), ('Absent', 'Absent'), ('Leave', 'Leave'), ('Duty', 'Duty')], default='absent', max_length=50)),
                ('location', models.CharField(blank=True, max_length=300, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.user')),
            ],
        ),
    ]
