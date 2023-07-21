from django.shortcuts import render,redirect
from products.models import Product

from wishlist.models import Wishlist
from django.views.decorators.cache import cache_control
from django.http.response import JsonResponse
from cart.models import Cart
# Create your views here.
from django.contrib.auth.models import User



from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import AnonymousUser

def product_detail(request, product_id):
    try:
        prod = Product.objects.get(slug=product_id)
    except Product.DoesNotExist:
        return redirect('shop')

    if request.method == 'POST':
        prod_id = request.POST.get('prod_id')
        product = get_object_or_404(Product, pk=prod_id)
        product_quantity = prod.quantity
        return JsonResponse({'product_id': product.id, 'product_quantity': product_quantity})

    related = Product.objects.all()
    cart = None  # Set cart as None by default

    # Check if the user is authenticated and not anonymous
    if request.user.is_authenticated and not isinstance(request.user, AnonymousUser):
        cart = Cart.objects.filter(user=request.user, product=prod)

    context = {
        'allpro': related,
        'pro_detail': prod,
        'cart': cart
    }
    
    return render(request, 'product-detail.html', context)




