# In admin.py
from django.contrib import admin
from .models import PDFRecord

@admin.register(PDFRecord)
class PDFRecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'image_url', 'created_at')
