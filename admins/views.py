
from django.views.generic import CreateView

from .forms import CategoryForm
from .models import Category


class CategoryCreate(CreateView):
    model = Category
    template_name = 'seller/category.html'
    form_class = CategoryForm
    success_url = 'books'
