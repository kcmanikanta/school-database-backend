from django.urls import path
from .views import addResult, StudentMarksView, ResultView, PublishResultView, PublishedResultsView

app_name = 'results'

urlpatterns = [
    path('add/', addResult.as_view(), name='add-result'),
    path('list/', StudentMarksView.as_view(), name='student-marks-list'),
    path('update/', ResultView.as_view(), name='update-result'),
    path('publish/', PublishResultView.as_view(), name='publish-result'),
    path('published-results/', PublishedResultsView.as_view(), name='published-results'), 
]


