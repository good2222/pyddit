from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    
    path('set-role/<str:role>/', views.set_role, name='set_role'),
    
    path('announcements/', views.announcements_list, name='announcements_list'),
    path('announcements/<int:pk>/', views.announcement_detail, name='announcement_detail'),
    path('announcements/<int:pk>/edit/', views.announcement_edit, name='announcement_edit'),
    path('announcements/<int:pk>/delete/', views.announcement_delete, name='announcement_delete'),
    path('announcements/<int:pk>/like/', views.announcement_like, name='announcement_like'),

    path('g/<str:section_name>/', views.mock_section, name='mock_section'),
]
