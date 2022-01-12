from django.db import models
from authapp.models import User
from bookstore.common.abstact_models import Abstractmodels
from admins.models import Category


class Book(Abstractmodels):
    name = models.CharField(max_length=120, verbose_name='Book Name')
    author = models.CharField(max_length=120, verbose_name='Author')
    price = models.PositiveIntegerField(default=0)
    publisher = models.CharField(max_length=120, verbose_name='Publisher')
    language = models.CharField(max_length=120, verbose_name='language')
    country_of_origin = models.CharField(max_length=120, verbose_name='Country of Origin')
    details = models.CharField(max_length=1000, verbose_name='Details of Book')
    image = models.ImageField(upload_to='book_images')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='seller')
    stock = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-created_date']

    def __str__(self):
        return self.name


class BookStock(Abstractmodels):
    stock_available = models.PositiveIntegerField(default=0, help_text='No: of Books Available')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='bookstock')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='stockadder')

    class Meta:
        ordering = ['-created_date']

    def __str__(self):
        return str(self.book)

