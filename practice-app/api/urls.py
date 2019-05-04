from django.urls import path
from rest_framework.documentation import include_docs_urls

from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginAPIView.as_view(), name='login'),
    path('investments/total_profit', views.TotalProfitAPIView.as_view(), name='total profit'),
    path('parity/<date>/', views.ParityView.as_view(), name='parity history'),
    path('doc/', include_docs_urls('Practice-App API'))
]