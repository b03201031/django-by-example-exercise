from django.shortcuts import render, get_object_or_404

from .models import Category, Product
# Create your views here.

from cart.forms import CartAddProductForm



def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)

    if category_slug:
        category = get_object_or_404(categories, slug=category_slug)
        products = products.filter(category=category)

    TEMPLATE_PATH = 'shop/product/list.html'
    CONTEXT = {
        'category': category,
        'categories': categories,
        'products': products,
    }

    return render(request, TEMPLATE_PATH, context=CONTEXT)


def product_detail(request, product_id, slug):
    product = get_object_or_404(Product, id=product_id, slug=slug, available=True)
    cart_product_form = CartAddProductForm()
    TEMPLATE_PATH = 'shop/product/detail.html'
    CONTEXT = {
        'product': product,
        'cart_product_form': cart_product_form,
    }

    return render(request, TEMPLATE_PATH, context=CONTEXT)

