from django.contrib import admin
from authapp.models import User

class UserAdmin(admin.ModelAdmin):
    list_display = [
        'username', 'is_seller', 'is_customer', 'is_superuser'
    ]
    list_filter = ('is_seller', 'is_customer')


admin.site.register(User, UserAdmin)
