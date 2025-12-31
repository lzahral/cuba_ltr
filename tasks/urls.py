from django.urls import path
from .views import *


urlpatterns = [
    path("new/", TaskCreateView.as_view(), name="new_task"),
    path("list/",  TaskListView.as_view(), name="tasks"),
    path("list/<int:pk>/", TaskDetailView.as_view(), name="task_detail"),
    path("list/edit/<int:pk>/", TaskUpdateView.as_view(), name="edit_task"),
    path("list/<int:pk>/delete/", TaskDelete.as_view(), name="delete_task"), 
    path("tasks/<int:task_id>/submit/",TaskSubmissionCreateView.as_view(),name="task_submit"),
]
