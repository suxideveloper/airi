from . import views
from django.urls import path


urlpatterns = [
    path('kurish/', views.kurish, name='kurish'),
    path('test/', views.test, name='test'),
]