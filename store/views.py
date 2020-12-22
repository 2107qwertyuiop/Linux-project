from django.shortcuts import render

from .models import *



# Create your views here.

#gen html to screen
def store(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'store/store.html', context)

def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        # if customer does not already exist, create the new one
        order, created = Order.objects.get_or_create(customer=customer,complete =  False)
        # get all single item of order
        items = order.orderitem_set.all()
    else:
        items =[]
        order = {'get_cart_total' : 0, 'get_cart_items' : 0}
    context = {'items':items, 'order':order}
    return render(request, 'store/cart.html', context)

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        # if customer does not already exist, create the new one
        order, created = Order.objects.get_or_create(customer=customer,complete =  False)
        # get all single item of order
        items = order.orderitem_set.all()
    else:
        items =[]
        order = {'get_cart_total' : 0, 'get_cart_items' : 0}
    context = {'items':items, 'order':order}
    return render(request, 'store/checkout.html', context)