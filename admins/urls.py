from django.urls import path
from admins import views

urlpatterns = [
    path('categoryadd', views.CategoryCreate.as_view(), name='addcategory'),
    ]