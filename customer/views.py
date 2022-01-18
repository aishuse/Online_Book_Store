from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.views.generic import ListView, DetailView, TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib import messages
from datetime import datetime, timedelta
import stripe

from admins.models import Category
from customer.forms import ContactFormEmail
from customer.models import Cart, Address, BookBuy, Request_Book
from seller.models import Book
from authapp.decorators import customer_required

stripe.api_key = settings.STRIPE_SECRET_KEY


class CustHome(TemplateView):
    template_name = 'customer/index.html'


@method_decorator([login_required, customer_required], name='dispatch')
class FullBooks(ListView):
    model = Book
    template_name = 'customer/bookslist.html'
    context_object_name = 'books'


@method_decorator([login_required, customer_required], name='dispatch')
class BookDetails(DetailView):
    model = Book
    template_name = 'customer/bookdetail.html'
    context_object_name = 'books'


@method_decorator([login_required, customer_required], name='dispatch')
class AddToCart(TemplateView):
    model = Cart

    def get(self, request, *args, **kwargs):
        pk = kwargs['pk']
        book = Book.objects.get(pk=pk)
        if Cart.objects.filter(item=book, user=self.request.user, status='incart').exists():
            pass

        else:
            cart = Cart.objects.create(item=book, user=self.request.user)
            cart.save()
            print('book added')
        return redirect('books')


def cart_plus(request, *args, **kwargs):
    id = kwargs['pk']
    cart = Cart.objects.get(id=id)
    cart.quantity += 1
    cart.save()
    return redirect('mycart')


def cart_minus(request, *args, **kwargs):
    id = kwargs['pk']
    cart = Cart.objects.get(id=id)
    cart.quantity -= 1
    cart.save()
    if cart.quantity < 1:
        return redirect('removeitem', cart.id)
    return redirect('mycart')


# @method_decorator([login_required, customer_required], name='dispatch')
class ViewMyCart(TemplateView):
    model = Cart
    template_name = 'customer/mycart.html'
    context = {}

    def get(self, request, *args, **kwargs):
        mycart = self.model.objects.filter(user=self.request.user, status='incart')
        total = 0
        for cart in mycart:
            if cart.quantity > cart.item.stock:
                cart.quantity = cart.item.stock
                cart.save()
            if (cart.quantity == 0) & (cart.item.stock != 0):
                cart.quantity = 1
                cart.save()
            total += cart.item.price * cart.quantity

        self.context['items'] = mycart
        self.context['total'] = total
        return render(request, self.template_name, self.context)


@method_decorator([login_required, customer_required], name='dispatch')
class RemoveFromCart(TemplateView):
    model = Cart

    def get(self, request, *args, **kwargs):
        pk = kwargs['pk']
        cart = self.model.objects.get(pk=pk)
        cart.status = 'cancelled'
        cart.save()
        return redirect('mycart')


# @method_decorator([login_required, customer_required], name='dispatch')
def CheckoutView(request):
    address = Address.objects.filter(user=request.user)
    addr = []
    for i in address:
        data = {}
        data['name'] = i.name
        data['mob'] = i.mob_no
        data['address'] = '{}, {}, {}, {}, India, {} '.format(i.house, i.street, i.town, i.state, i.pin)
        data['landmark'] = '{}'.format(i.landmark)
        data['id'] = i.id
        addr.append(data)
    print('addresses :', addr)
    context = {
        'address': addr
    }
    if request.method == "POST":
        print(request.POST)
        x = request.POST
        new_address = Address()
        new_address.user = request.user
        new_address.name = x['name']
        new_address.mob_no = x['mob_no']
        new_address.house = x['house']
        new_address.street = x['street_address']
        new_address.town = x['town']
        new_address.state = x['state']
        new_address.pin = x['pin']
        new_address.landmark = x['landmark']
        if (Address.objects.filter(house=x['house'], pin=x['pin']).exists()):
            print('already exists')
        else:
            new_address.save()
            return redirect("checkout")
    return render(request, 'customer/checkout.html', context)


# @method_decorator([login_required, customer_required], name='dispatch')
def placeorder(request, *args, **kwargs):
    cart_item = Cart.objects.filter(user=request.user, status='incart')
    address = Address.objects.get(id=kwargs.get('pk'))
    ad = '{},{},{}, {}, {}, {}, India, {} '.format(address.name, address.mob_no, address.house, address.street,
                                                   address.town, address.state, address.pin, address.landmark)
    for i in cart_item:
        if i.item.stock == 0:
            i.status = 'cancelled'
        else:
            order = BookBuy()
            if (BookBuy.objects.filter(item=Book.objects.get(id=i.item.id), user=request.user, address=ad,
                                       status='pending')).exists():
                print('already exists')
            else:
                order.item = Book.objects.get(id=i.item.id)
                order.user = request.user
                order.seller = Book.objects.get(id=i.item.id).user
                order.address = ad
                order.quantity = i.quantity
                order.price = (i.item.price) * (i.quantity)
                order.expected_delivery = datetime.now() + timedelta(days=7)
                order.status = 'pending'
                order.save()
    total = 0
    data = []
    for i in cart_item:
        context = {}
        item = Book.objects.get(id=i.item_id)
        context['image'] = item.image
        context['name'] = item.name
        context['quantity'] = i.quantity
        context['price'] = item.price
        context['address'] = ad
        total += i.item.price * i.quantity
        context['total'] = total
        data.append(context)
    return render(request, 'customer/order_summery.html', {'data': data, 'address': ad, 'total': total})


class GatewayView(TemplateView):
    template_name = "customer/stripe.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_products = Cart.objects.filter(user=self.request.user, status='incart')
        total = 0
        for cart in cart_products:
            total += cart.item.price * cart.quantity
        context['total'] = total
        context['amount'] = total * 100
        print("total=", total)
        context['key'] = settings.STRIPE_PUBLISHABLE_KEY
        return context


def charge(request, amount=None, *args, **kwargs):
    cart_products = Cart.objects.filter(user=request.user, status='incart')
    total = 0
    for cart in cart_products:
        total += cart.item.price * cart.quantity
    if request.method == "POST":
        payment_intent = stripe.PaymentIntent.create(
            amount=total*100,
            currency="INR",
            description="book purchase",
            payment_method_types=["card"],
        )
        cart_item = Cart.objects.filter(user=request.user, status='incart')
        buy = BookBuy.objects.filter(status="pending", user=request.user)
        for i in cart_item:
            i.status = 'cancelled'
            i.item.stock = i.item.stock - i.quantity
            i.item.save()
            i.save()
        for i in buy:
            i.status = 'orderplaced'
            i.save()
        return render(request, 'customer/payment.html', payment_intent)
    return render(request, 'customer/payment.html')


@method_decorator([login_required, customer_required], name='dispatch')
class MyOrders(ListView):
    model = BookBuy
    template_name = 'customer/myorders.html'
    context_object_name = "orders"

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = self.model.objects.filter(user=self.request.user)
        return queryset

@login_required
def request_books(request):
    if request.method == "POST":
        user = request.user
        book_name = request.POST['book_name']
        author = request.POST['author']
        book = Request_Book(user=user, book_name=book_name, author=author)
        book.save()
        messages.success(request, 'Request Send')
        return render(request, "customer/request_books.html")
    return render(request, "customer/request_books.html")

@login_required
def contactsendmail(request):
    if request.method == 'GET':
        form = ContactFormEmail()
    else:
        form = ContactFormEmail(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            send_mail(subject, message, email, ['booklandz911@gmail.com', email])
            messages.success(request, 'message send')
            return redirect('contactus')
    return render(request, 'customer/contactpage.html', {'form': form})

@login_required
def bookSearchView(request):
    if request.method == "POST":
        query_name = request.POST.get('name', None)
        if query_name:
            results = Book.objects.filter(name__contains=query_name)
            return render(request, 'customer/searchbook.html', {"results": results})
    return render(request, 'customer/searchbook.html')


@method_decorator([login_required, customer_required], name='dispatch')
class ListCategory(ListView):
    model = Category
    template_name ='customer/categorylist.html'
    context_object_name = 'category'

@method_decorator([login_required, customer_required], name='dispatch')
class Categories(ListView):
    model = Category
    template_name = 'customer/categorydetail.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        obj = Category.objects.get(pk=self.kwargs['pk'])
        cat = obj.category.all()
        context['cat'] = cat
        context['obj'] = obj
        return context





