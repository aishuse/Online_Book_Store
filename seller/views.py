from django.db.models import Sum
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView, TemplateView

from customer.forms import OrderUpdateForm
from customer.models import BookBuy, Request_Book
from seller.forms import AddBookForm, BookStockForm
from seller.models import Book, BookStock
from authapp.decorators import seller_required



@method_decorator([login_required, seller_required], name='dispatch')
class BookCreate(CreateView):
    model = Book
    template_name = 'seller/book_create.html'
    form_class = AddBookForm
    success_url = 'stockadd'
    context_object_name = 'books'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(BookCreate, self).form_valid(form)


@method_decorator([login_required, seller_required], name='dispatch')
class StockAdd(CreateView):
    model = BookStock
    template_name = 'seller/stock.html'
    form_class = BookStockForm
    success_url = 'mybooks'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        book = Book.objects.get(id=form.data.__getitem__('book'))
        stockavailable = form.data.__getitem__('stock_available')
        book.stock = book.stock + int(stockavailable)
        book.save()
        return super(StockAdd, self).form_valid(form)


@method_decorator([login_required, seller_required], name='dispatch')
class OutofStock(ListView):
    model = Book
    context_object_name = 'books'
    template_name = 'seller/outofstock.html'

    def get_queryset(self):
        return Book.objects.filter(user=self.request.user, stock=0)


@method_decorator([login_required, seller_required], name='dispatch')
class MyBooks(ListView):
    model = Book
    template_name = 'seller/my_books.html'
    context_object_name = 'books'

    def get_queryset(self):
        return Book.objects.filter(user=self.request.user)


@method_decorator([login_required, seller_required], name='dispatch')
class MyBooksDetails(DetailView):
    model = Book
    template_name = 'seller/book_detail.html'
    context_object_name = 'books'

    # def get_context_data(self, **kwargs):
    #     # Call the base implementation first to get a context
    #     context = super().get_context_data(**kwargs)
    #     # import pdb
    #     # pdb.set_trace()
    #     book = self.get_object()    # fetch the object using pk from url
    #     stock = book.bookstock.aggregate(Sum("stock_available"))  # bookstock is the related name of BookStock model
    #     context['stock'] = stock
    #     return context


@method_decorator([login_required, seller_required], name='dispatch')
class BookUpdateView(UpdateView):
    model = Book
    template_name = 'seller/update_book.html'
    form_class = AddBookForm
    success_url = '/seller/mybooks'


@method_decorator([login_required, seller_required], name='dispatch')
class BookDelete(DeleteView):
    model = Book
    template_name = 'seller/delete.html'
    success_url = '/seller/mybooks'


@method_decorator([login_required, seller_required], name='dispatch')
class StockView(ListView):
    model = BookStock
    template_name = 'seller/bookstock.html'
    context_object_name = 'stocks'

    def get_queryset(self):
        return BookStock.objects.filter(user=self.request.user)


@method_decorator([login_required, seller_required], name='dispatch')
class ViewOrders(TemplateView):
    model = BookBuy
    template_name = "seller/orders.html"

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        count = self.model.objects.filter(status='orderplaced', seller=self.request.user).count()
        context['order_count'] = count
        context['orders'] = self.model.objects.filter(status='orderplaced', seller=self.request.user)

        dispatch = self.model.objects.filter(status='dispatch', seller=self.request.user)
        context['dispatch'] = dispatch
        context['dispatch_count'] = dispatch.count()

        intransit = self.model.objects.filter(status='intransit', seller=self.request.user)
        context['intransit'] = intransit
        context['intransit_count'] = intransit.count()

        delivered = self.model.objects.filter(status='delivered', seller=self.request.user)
        context['delivered'] = delivered
        context['delivered_count'] = delivered.count()

        ordercancelled = self.model.objects.filter(status='ordercancelled', seller=self.request.user)
        context['ordercancelled'] = ordercancelled
        context['ordercancelled_count'] = ordercancelled.count()
        return context


@method_decorator([login_required, seller_required], name='dispatch')
class ViewSingleCustomer(DetailView):
    model = BookBuy
    template_name = "seller/customer_order_detail.html"
    context_object_name = "order"


@method_decorator([login_required, seller_required], name='dispatch')
class OrderUpdateView(UpdateView):
    model = BookBuy
    template_name = 'seller/orderupdate.html'
    form_class = OrderUpdateForm
    success_url = reverse_lazy("customerorders")


def see_requested_books(request):
    requested_book = Request_Book.objects.all()
    requested_books_count = requested_book.count()
    return render(request, "seller/see_requested_books.html", {'requested_book': requested_book, 'requested_books_count':requested_books_count})





