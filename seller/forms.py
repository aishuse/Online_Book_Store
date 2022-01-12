from django import forms
from .models import Book, BookStock


class AddBookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['name', 'author', 'price', 'publisher', 'details', 'language', 'country_of_origin', 'image', 'category']
        widgets = {

            'name': forms.TextInput(attrs={"class": "form-control"}),
            'author': forms.TextInput(attrs={"class": "form-control"}),
            'price': forms.NumberInput(attrs={"class": "form-control"}),
            'publisher': forms.TextInput(attrs={"class": "form-control"}),
            'language': forms.TextInput(attrs={"class": "form-control"}),
            'country_of_origin': forms.TextInput(attrs={"class": "form-control"}),
            'details': forms.Textarea(attrs={"class": "form-control"}),

        }


class BookStockForm(forms.ModelForm):
    class Meta:
        model = BookStock
        fields = ['stock_available', 'book']
        widgets = {
            'stock_available': forms.NumberInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user') # Important to do this
        # If you dont, calling super will fail because the init does
        # not expect, user among the fields.
        super().__init__(*args, **kwargs)
        self.fields['book'].queryset = Book.objects.filter(user=user)






