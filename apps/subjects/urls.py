from django.urls import path
from .views import SubjectByClassView 

urlpatterns = [
    path('subject-by-class/', SubjectByClassView.as_view(), name='subject-by-class'),
]