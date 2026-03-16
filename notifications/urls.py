from django.urls import path
from . import views

urlpatterns = [
    path('', views.NotificationListView.as_view(), name='notifications'),
    path('mark-read/<int:pk>/', views.mark_as_read, name='mark_notification_read'),
]
