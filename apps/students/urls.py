from django.urls import path
from .views import StudentsAdd, StudentsList, StudentUpdate,AdminStudentAddView
urlpatterns = [
    path('add/', StudentsAdd.as_view(), name = 'students add'),
    path('list/', StudentsList.as_view(), name = 'students list'),
    path('update/<int:pk>/', StudentUpdate.as_view(), name='student update'),
    path('admin/add-student/', AdminStudentAddView.as_view(), name='admin-add-student'),

]