from django.db import models
from authapp.models import User
from bookstore.common.abstact_models import Abstractmodels
from seller.models import Book
import datetime
from django.core.validators import MinValueValidator


class Cart(Abstractmodels):
    INCART = 'incart'
    CANCELLED = 'cancelled'

    options = (
        (INCART, 'incart'),
        (CANCELLED, 'cancelled'),
    )
    item = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='item')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    status = models.CharField(max_length=120, choices=options, default='incart')
    quantity = models.IntegerField(default=1)

    class Meta:
        ordering = ['-created_date']


    def __str__(self):
        return self.item.name


class Address(Abstractmodels):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    mob_no = models.CharField(max_length=30)
    house = models.CharField(max_length=150)
    street = models.CharField(max_length=150)
    town = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pin = models.CharField(max_length=30)
    landmark = models.CharField(max_length=150)

    class Meta:
        ordering = ['-created_date']

    def __str__(self):
        return self.name


class BookBuy(Abstractmodels):
    PENDING = 'pending'
    ORDERPLACED = 'orderplaced'
    DISPATCH = 'dispatch'
    INTRANSIT = 'intransit'
    DELIVERED = 'delivered'
    ORDERCANCELLED = 'ordercancelled'

    options = ((PENDING, 'pending'),
               (ORDERPLACED, 'orderplaced'),
               (DISPATCH, 'dispatch'),
               (INTRANSIT, 'intransit'),
               (DELIVERED, 'delivered'),
               (ORDERCANCELLED, "ordercancelled")
               )

    quantity = models.PositiveIntegerField(default=1, help_text='No: of Books You Want To Buy')
    item = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='buybook', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='buyuser')
    address = models.CharField(max_length=120)
    seller = models.CharField(max_length=250, default=None)
    status = models.CharField(max_length=120, choices=options, default='orderplaced')
    expected_delivery = models.DateField(null=True, blank=True, validators=[MinValueValidator(datetime.date.today)])

    class Meta:
        ordering = ['-created_date']

    def __str__(self):
            return self.item.name


class Request_Book(Abstractmodels):
    book_name = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-created_date']

    def __str__(self):
        return self.book_name


