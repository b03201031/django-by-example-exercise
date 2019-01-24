from django.shortcuts import render
from .models import OrderItem
from .forms import OrderCreateForm
from .task import order_created
from cart.cart import Cart

# Create your views here.

def order_create(request):
    cart = Cart(request)
    
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order, product=item['product'],
                                         price=item['price'], quantity=item['quantity'])

            cart.clear()
            order_created.delay(order.id)
            TEMPLATE_PATH = 'orders/order/created.html'     
            context = {
                'order': order,
            }

            return render(request, TEMPLATE_PATH, context=context)

    else:
        form = OrderCreateForm()

    TEMPLATE_PATH = 'orders/order/create.html'
    context = {
        'form': form,
    }

    return render(request, TEMPLATE_PATH, context=context)