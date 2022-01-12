from django.contrib import admin
from customer.models import Cart, BookBuy, Address, Request_Book


class BookBuyAdmin(admin.ModelAdmin):
    list_display = [
         'item', 'quantity', 'user', 'seller', 'status', 'created_date'
    ]
    list_filter = ('item', 'seller', 'status')


class CartAdmin(admin.ModelAdmin):
    list_display = [
         'item', 'quantity', 'user', 'status'
    ]
    list_filter = ('item', 'quantity', 'user')


class AddressAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'pin', 'user'
    ]
    list_filter = ('name', 'pin', 'user')


class Request_BookAdmin(admin.ModelAdmin):
    list_display = [
        'book_name', 'author', 'user'
    ]
    list_filter = ('book_name', 'author', 'user')


admin.site.register(BookBuy, BookBuyAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(Request_Book, Request_BookAdmin)