from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('translate/', views.translate, name='translate'),
    path('translateform/', views.translate_form, name='translate_form'),
]
