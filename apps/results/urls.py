from django.urls import path, re_path
from .views import addResult, ResultList

app_name = 'results'

urlpatterns = [
    path('add/', addResult.as_view(), name='declare_result'),
    path('list/', ResultList.as_view(), name='declare_result'),
]