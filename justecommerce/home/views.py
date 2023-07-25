
from django.shortcuts import render,redirect

from django.views.decorators.cache import cache_control,never_cache

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout as dj_logout

from products.models import Product
from categories.models import category
from django.contrib.auth.models import User
from brand.models import Brand
from django.http.response import JsonResponse
from django.template.loader import render_to_string
from django.http import HttpRequest
from cart.models import Cart
from wishlist.models import Wishlist
from django.db.models import Sum,Count




def home(request):
    if request.user.is_superuser:
        return redirect('dashboard')

    if request.user.is_authenticated:

        cartcount = Cart.objects.filter(user=request.user).aggregate(cartcount=Count('id'))['cartcount']
        wishcount=Wishlist.objects.filter(user=request.user).aggregate(wishcount=Count('id'))['wishcount']
    else:
        cartcount=0
        wishcount=0
    
    cate=category.objects.all()
    brands=Brand.objects.all()
    print(cartcount,wishcount,'ccccccccccccccccccccccccccccccccc')

    sort_option = request.GET.get('sort')
    search_query = request.GET.get('search')
    products = Product.objects.all()  # Fetch your product list from the database

    if sort_option == 'atoz':
        sorted_products = products.order_by('product_name')  # Sort products by name in ascending order
       
    elif sort_option == 'ztoa':
        sorted_products = products.order_by('-product_name')  # Sort products by name in descending order
       
    elif sort_option == 'lowtohigh':
        sorted_products = products.order_by('product_price')  # Sort products by price in ascending order
       
    elif sort_option == 'hightolow':
        sorted_products = products.order_by('-product_price')  # Sort products by price in descending order
       
    else:
        sorted_products = products  # Default case, no sorting applied
    if search_query:
        sorted_products = sorted_products.filter(product_name__icontains=search_query)
      
    # Render the updated product list HTML or return as JSON response
    if is_ajax(request=request):
        return JsonResponse({'html': render_to_string('index.html',{'products_list':sorted_products,'cat':cate,'brand':brands,'cartcount':cartcount,'wishcount':wishcount})})
    else:
        return render(request,'index.html',{'products_list':sorted_products,'cat':cate,'brand':brands,'cartcount':cartcount,'wishcount':wishcount})

   

    
   


    
    # return render(request,'index.html',{'products_list':pro,'categories':cate,'brands':brands})

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


def shop(request):
    if request.user.is_superuser:
                return redirect('dashboard')

    
    cat=category.objects.all()
    bra=Brand.objects.all()

    sort_option = request.GET.get('sort')
    search_query = request.GET.get('search')
    products = Product.objects.all()  # Fetch your product list from the database

    if sort_option == 'atoz':
        sorted_products = products.order_by('product_name')  # Sort products by name in ascending order
       
    elif sort_option == 'ztoa':
        sorted_products = products.order_by('-product_name')  # Sort products by name in descending order
       
    elif sort_option == 'lowtohigh':
        sorted_products = products.order_by('product_price')  # Sort products by price in ascending order
       
    elif sort_option == 'hightolow':
        sorted_products = products.order_by('-product_price')  # Sort products by price in descending order
       
    else:
        sorted_products = products  # Default case, no sorting applied
    if search_query:
        sorted_products = sorted_products.filter(product_name__icontains=search_query)
      
    # Render the updated product list HTML or return as JSON response
    if is_ajax(request=request):
        return JsonResponse({'html': render_to_string('product.html',{'products_list':sorted_products,'cat':cat,'brand':bra})})
    else:
        return render(request,'product.html',{'products_list':sorted_products,'cat':cat,'brand':bra})

    
    
    




@login_required(login_url='user_login')
def user_logout(request):
    if request.user.is_authenticated:
        
        dj_logout(request)
        return redirect('user_login')
    else:
        return redirect('home')






def about(request):

    return render(request,'about.html')


def blog(request):

    return render(request,'blog.html')

