from django.urls import path, include
from authapp import views

urlpatterns = [

    path('multisignup', views.MultiSignup.as_view(), name='multisignup'),

]