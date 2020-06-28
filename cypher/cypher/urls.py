from django.urls import path

from .views import submit_task, task_view

urlpatterns = [
    path('submit/', submit_task),
    path('submit/<str:task_hash>/', submit_task),
    path('view/', task_view),
    path('view/<str:task_hash>/', task_view),
]
