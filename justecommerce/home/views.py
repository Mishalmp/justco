
from django.shortcuts import render,redirect

from django.views.decorators.cache import cache_control,never_cache

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout as dj_logout

from products.models import Product
from categories.models import category
from django.contrib.auth.models import User
from brand.models import brand


def home(request):

    pro=Product.objects.all()
    cate=category.objects.all()
    brands=brand.objects.all()

   

    
    return render(request,'index.html',{'products_list':pro,'categories':cate,'brands':brands})





def shop(request):
    
    sort = request.GET.get('sort')
    
    if sort == 'atoz':
        
        pro = Product.objects.all().order_by('product_name')

    elif sort == 'ztoa':
        pro = Product.objects.all().order_by('-product_name')

    elif sort == 'ltoh':
        pro = Product.objects.all().order_by('product_price')

    elif sort == 'htol':
        pro = Product.objects.all().order_by('-product_price')

    else:
        pro = Product.objects.all()
    

    
    return render(request,'product.html',{'products_list':pro})





# @login_required(login_url='user_login')
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

