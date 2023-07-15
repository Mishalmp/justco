from tkinter import Image
from django.shortcuts import render,redirect
from categories.models import category
from django.contrib import messages
from .models import Product as products, PriceFilter
from brand.models import brand
import logging
from django.contrib.auth.decorators import login_required

from django.http import JsonResponse
# Create your views here.
from django.core.files.uploadedfile import SimpleUploadedFile

import base64
import re
from PIL import Image
from io import BytesIO
from PIL import Image
import base64
from io import BytesIO




# Rest of your code.



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

# def main_view(request):
#     form = ImageForm(request.POST or None, request.FILES or None)
#     if form.is_valid():
#         form.save()
#         return JsonResponse({'message': 'works'})
#     context = {'form': form}
#     return render(request, 'templates/main.html', context)

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
        quantity = request.POST['quantity']

        # Validation
        if products.objects.filter(product_name=name).exists():
            return JsonResponse({'message': 'Product name already exists'})

        try:
            is_availables = request.POST.get('checkbox', False)
            if is_availables == 'on':
                is_availables = True
            else:
                is_availables = False
        except:
            is_availables = False

        if name == '' or price == '':
            return JsonResponse({'message': 'Name or Price field is empty'})

        if name.strip() == '':
            return JsonResponse({'message': 'Image Not Found'})

        if not image:
            return JsonResponse({'message': 'Image not uploaded'})

        category_obj = category.objects.get(id=category_id)
        brand_obj = brand.objects.get(brand_name=brandname)
        price_range_obj = PriceFilter.objects.get(id=price_range)

        # Save the product
        product = products(
            product_name=name,
            product_price=price,
            product_image=image,
            product_image2=image2,
            product_image3=image3,
            product_description=description,
            is_available=is_availables,
            brand=brand_obj,
            category=category_obj,
            price_range=price_range_obj,
            quantity=quantity
        )
        product.save()

        return JsonResponse({'message': 'Product created successfully'})

    return render(request, 'product/product.html')



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
        quantity = request.POST.get('quantity')

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
            messages.error(request,'Image Not Found')
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
        cat.quantity=quantity
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
    
    pro.quantity=0
    pro.is_available=False
    pro.save()

    return redirect('product')









