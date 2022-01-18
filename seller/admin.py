from django.contrib import admin
from seller.models import Category, BookStock, Book

class BookAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'author', 'price', 'category', 'stock', 'user'
    ]
    list_filter = ('name', 'author', 'user', 'category')


class BookStockAdmin(admin.ModelAdmin):
    list_display = [
        'book', 'stock_available', 'user'
    ]
    list_filter = ('book', 'stock_available', 'user')


admin.site.register(Book, BookAdmin)
admin.site.register(BookStock, BookStockAdmin)
