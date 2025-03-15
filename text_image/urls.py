from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('generate/', views.generate_image, name='generate'),
    path('result/<uuid:pk>/', views.result, name='result'),
    path('history/', views.HistoryListView.as_view(), name='history'),
    path('detail/<uuid:pk>/', views.RequestDetailView.as_view(), name='detail'),
    path('delete/<uuid:pk>/', views.RequestDeleteView.as_view(), name='delete'),
    path('test-styles/', views.test_styles, name='test_styles'),
] 