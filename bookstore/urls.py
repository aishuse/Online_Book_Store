from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from authapp import views


urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('authapp/', include('authapp.urls')),
    path('admins/', include('admins.urls')),
    path('seller/', include('seller.urls')),
    path('customer/', include('customer.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup/seller/', views.SellerSignUpView.as_view(), name='sellersignup'),
    path('accounts/signup/customer/', views.CustomerSignUpView.as_view(), name='customersignup'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
