from django.urls import path
from .views import PDFRecordCreateView, PDFRecordListView, PDFRecordDetailView

urlpatterns = [
    path('pdfrecords/', PDFRecordListView.as_view(), name='pdfrecord-list'),
    path('pdfrecords/create/', PDFRecordCreateView.as_view(), name='pdfrecord-create'),
    path('pdfrecords/<int:id>/', PDFRecordDetailView.as_view(), name='pdfrecord-detail'),
]
