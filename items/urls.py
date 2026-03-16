from django.urls import path
from . import views

urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('lost/', views.LostItemListView.as_view(), name='lost_items'),
    path('found/', views.FoundItemListView.as_view(), name='found_items'),
    path('report-lost/', views.ReportLostView.as_view(), name='report_lost'),
    path('report-found/', views.ReportFoundView.as_view(), name='report_found'),
    path('lost/<int:pk>/', views.LostItemDetailView.as_view(), name='lost_detail'),
    path('found/<int:pk>/', views.FoundItemDetailView.as_view(), name='found_detail'),
    path('lost/<int:pk>/delete/', views.LostItemDeleteView.as_view(), name='lost_delete'),
    path('found/<int:pk>/delete/', views.FoundItemDeleteView.as_view(), name='found_delete'),
]
