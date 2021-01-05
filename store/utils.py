import json
from .models import *


def cookieCart(request):
# load cart from cookie, if first load , create new cart dictionary in view
# must have try except cause there is some product was deleted from database but still have in cookie data
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}
        print('Cart: ', cart)

    # create empty info for guest user first, then take data from cookie to fill in
    items = []
    order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
    cartItems = order['get_cart_items']

    # loop through (KEY) in cart object to get total item, plus to cartItems to gen to screen
    for i in cart:

        #
        try:
            cartItems += cart[i]['quantity']

            # find product in database that have id similar to cookie
            product = Product.objects.get(id=i)
            total = (product.price * cart[i]['quantity'])

            order['get_cart_total'] += total  # price
            order['get_cart_items'] += cart[i]['quantity']  # number

            # build item in cart base on product id in cookie
            item = {
                'id': product.id,
                'product': {
                    'id': product.id,
                    'name': product.name,
                    'price': product.price,
                    'imageURL': product.imageURL,
                },
                'quantity': cart[i]['quantity'],
                'digital' : product.digital,
                'get_total': total,
            }
            items.append(item)

            if product.digital == False:
                order['shipping'] = True
        except:
            pass
    return {'cartItems': cartItems, 'order' :order, 'items' :items} 

#use this function to gen data of items on user's cart to screen
def cartData(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        # if customer does not already exist, create the new one
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        # get all single item of order
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']
    return{'cartItems': cartItems, 'order': order, 'items': items}

def guestOrder(request, data):
# user info take from form
    name = data['form']['name']
    email = data['form']['email']

    # take items data from cookie
    cookieData = cookieCart(request)
    items = cookieData['items']

    customer, created = Customer.objects.get_or_create(
        email=email,
    )

    customer.name = name
    customer.save()

    order = Order.objects.create(
        customer=customer,
        complete=False
    )

    for item in items:
        product = Product.objects.get(id=item['id'])
        orderItems = OrderItem.objects.create(
            product=product,
            order=order,
            quantity=item['quantity']
        )
    return customer,order