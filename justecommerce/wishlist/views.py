from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required

# Create your views here.
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from wishlist.models import Wishlist
from django.views.decorators.cache import cache_control
from django.http.response import JsonResponse
from products.models import Product
# from django.contrib.auth.models import AnonymousUser
from cart.models import Cart
# Create your views here.
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required(login_url='user_login')
def wishlist(request):
    if request.user.is_superuser:
        return redirect('dashboard')
  
    
    wishlist = Wishlist.objects.filter(user = request.user)
    cart = Cart.objects.filter(user=request.user)

    context = {
        'wishlist' : wishlist,
        'cart':cart
    }
    return render(request, 'user/wishlist.html',context)

# Add to wishlist
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def add_wishlist(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            prod_id = request.POST.get('prod_id')
           
            product_check = Product.objects.get(id = prod_id)
            
  
          
            if(product_check):
                if(Wishlist.objects.filter(user = request.user, product = product_check)):
                    return JsonResponse({'status' : "Product already in wishlist"})
                else:
                    Wishlist.objects.create(user=request.user, product = product_check)
                    return JsonResponse({'status' : "Product Added to in wishlist"})
            else:
                JsonResponse({'status' : "No such product"})
                
        else:
            return JsonResponse({'status' : "Login to continue"})
    else:
        return JsonResponse('something went wrong, reload page',safe=False)
    
# Remove wishlist
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def delete_wishlist(request,product_id):
    print(product_id,'11111111')
    
    product_id = product_id
    wishlist_items = Wishlist.objects.filter(user=request.user, product=product_id)
    if wishlist_items.exists():
        wishlist_items.delete()
    return redirect('wishlist')



