from django.shortcuts import render,redirect
from categories.models import category
from django.contrib import messages
from .models import Product as products, PriceFilter
from brand.models import brand
import logging
from django.contrib.auth.decorators import login_required


# Create your views here.

# Product
@login_required(login_url='admin_login')
def product(request):
    if not request.user.is_superuser:
        return redirect('admin_login')
    prodec = products.objects.all().order_by('id')
    dict_list={
        'prod' : prodec,
        'category' : category.objects.all(),
        'brand': brand.objects.all(),
        'price_range' : PriceFilter.objects.all(),
       
    }
    return render(request ,'product/product.html',dict_list)

# Add Product
@login_required(login_url='admin_login')
def createproduct(request):
    if not request.user.is_superuser:
        return redirect('admin_login')
    if request.method == 'POST':
        name = request.POST['product_name']
        price = request.POST['product_price']
        image = request.FILES.get('product_image', None)
        image2 = request.FILES.get('product_image2', None)
        image3 = request.FILES.get('product_image3', None)
        price_range = request.POST.get('price_range')
        brandname = request.POST.get('brand')
        category_id = request.POST.get('category')
        description = request.POST['product_description']
       
        
# Validaiton
# one here
      
        if products.objects.filter(product_name=name).exists():
            messages.error(request, 'Product name already exists')
            return redirect('product')
        try:
            is_availables = request.POST.get('checkbox', False)
            if is_availables == 'on':
                is_availables = True
            else:
                is_availables = False
        except:
            is_availables = False

        if name == '' or price =='' :
            messages.error(request, "Name or Price field are empty")
            return redirect('product')
        if name.strip() =='':
            messages.error(request,'Image Not Found')
            return redirect('product')
        if not image:
            messages.error(request, "Image not uploaded")
            return redirect('product')

        categeryid  = category.objects.get(id=category_id)
        brandid = brand.objects.get(brand_name=brandname)
        prange = PriceFilter.objects.get(id=price_range)
# Save        
        produc = products(
            product_name=name,
            product_price=price,
            product_image=image,
            product_image2=image2,
            product_image3=image3,
            product_description = description,
            is_available = is_availables,
            brand = brandid,
            category = categeryid,
            price_range =prange,
           
        )
        produc.save()
        return redirect('product')
    return render(request, 'product/product.html' )


# Edit Product
@login_required(login_url='admin_login')
def editproduct(request,editproduct_id):
    if not request.user.is_superuser:
        return redirect('admin_login')
    if request.method == 'POST':
        pname = request.POST['product_name']
        pprice = request.POST['product_price']
        cdescription = request.POST['product_description']
        brandname = request.POST.get('brand')
        category_id = request.POST.get('category')
        price_range = request.POST.get('price_range')
        image2 = request.FILES.get('product_image2')
        image3 = request.FILES.get('product_image3')
# validation
        try:
            pro = products.objects.get(slug=editproduct_id)
            image = request.FILES.get('product_image')
            if image:
                pro.product_image = image
                pro.product_image2=image2
                pro.product_image3=image3
                pro.save()
        except products.DoesNotExist:
            messages.error(request,'Image Not Fount')
            return redirect('product')
#    one here
        try:
            is_availables = request.POST.get('checkbox', False)
            if is_availables == 'on':
                is_availables = True
            else:
                is_availables = False
        except:
            is_availables = False

        if pname == '' or pprice =='' :
            messages.error(request, "Name or Price field are empty")
            return redirect('product')
        if products.objects.filter(product_name=pname).exists() :
            check = products.objects.get(slug = editproduct_id)
            if pname == check.product_name:
                pass
            else:
                messages.error(request, 'Product name already exists')
                return redirect('product')
        
        cates = category.objects.get(id=category_id)
        produc = brand.objects.get(brand_name=brandname)
        prange = PriceFilter.objects.get(id=price_range)
# Save       
        cat = products.objects.get(slug=editproduct_id)
        cat.product_name = pname
        cat.price_range = prange
        cat.product_price = pprice
        cat.product_description = cdescription
        cat.is_available = is_availables
        cat.brand = produc
        cat.category = cates
       
        cat.save()
        return redirect('product')
    

# Search Product
@login_required(login_url='admin_login')
def search_product(request):
    if not request.user.is_superuser:
        return redirect('admin_login')
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            Prod = products.objects.filter(product_name__icontains=keyword).order_by('id')
            if Prod.exists():
                context = {
                    'prod': Prod,
                }
                return render(request, 'product/product.html',context)
            else:
                message = "Product not found."
                return render(request,'product/product.html', {'message': message})
        else:
            message = "Please enter a valid search keyword"
            return render(request, 'product/product.html', {'message': message})
    else:
        return render(request, '404.html')




def deleteproduct(request,deleteproduct_slug):
    if not request.user.is_superuser:
        return redirect('admin_login')
    pro = products.objects.get(slug=deleteproduct_slug)
    
    # pro.delete()

    return redirect('product')









