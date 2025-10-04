from . import views
from django.urls import path


urlpatterns = [
    path('kurish/', views.kurish, name='kurish'),
    path('test/<int:son>/', views.test, name='test'),
]