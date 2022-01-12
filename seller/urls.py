from django.urls import path
from seller import views

urlpatterns = [
    path('bookadd', views.BookCreate.as_view(), name='bookadd'),
    path('stockadd', views.StockAdd.as_view(),name='stockadd'),
    path('mybooks', views.MyBooks.as_view(), name='mybooks'),
    path('mybookdetails/<int:pk>', views.MyBooksDetails.as_view(),name='mybookdetails'),
    path('bookupdate/<int:pk>', views.BookUpdateView.as_view(), name= 'bookupdate'),
    path('bookdelete/<int:pk>', views.BookDelete.as_view(),name='bookdelete'),
    path('stockavailable', views.StockView.as_view(), name='stockavailable'),
    path('outofstock',views.OutofStock.as_view(),name='outofstock'),
    path("orders/list", views.ViewOrders.as_view(), name='customerorders'),
    path('orders/change/<int:pk>', views.OrderUpdateView.as_view(), name='orderchange'),
    path("orders/view/<int:pk>", views.ViewSingleCustomer.as_view(), name="cust_single_order"),
    path("see_requested_books/", views.see_requested_books, name="see_requested_books"),


]