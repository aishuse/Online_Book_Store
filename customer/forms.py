from .models import BookBuy, Request_Book
from django import forms


class BookBuyForm(forms.ModelForm):
    class Meta:
        model = BookBuy
        fields = ['quantity', 'address']


class OrderUpdateForm(forms.ModelForm):
    class Meta:
        model = BookBuy
        fields = ['status', 'expected_delivery']
        widgets = {
            "status": forms.Select(attrs={"class": "form-select"}),
            "expected_delivery": forms.DateInput(attrs={"type": "date"}),
        }


class Request_BookForm(forms.ModelForm):
    class Meta:
        model = Request_Book
        fields = ['book_name', 'author']

        widgets = {
            'book_name': forms.TextInput(attrs={"class": "form-control"}),
            'author': forms.TextInput(attrs={"class": "form-control"}),

        }


class ContactFormEmail(forms.Form):
    email = forms.EmailField(required=True)
    subject = forms.CharField(required=True)
    message = forms.CharField(required=True, widget=forms.Textarea)


