from django.shortcuts import render,redirect
from products.models import Product

from wishlist.models import Wishlist
from django.views.decorators.cache import cache_control
from django.http.response import JsonResponse
# Create your views here.



def product_detail(request,product_id):

    try:
        prod=Product.objects.get(slug=product_id)
    except Product.DoesNotExist:
        return render(request,'error/index.html')


    if request.method == 'POST':

        prod_id=request.POST.get('prod_id')
        product=Product.objects.get(product=prod_id)
        product_quantity=prod.quantity
        return JsonResponse({'product_id':product.id, 'product_quantity':product_quantity})

    related=Product.objects.all()

    context={
        'allpro':related,
        'pro_detail':prod

    }

    return render(request,'product-detail.html',context)




