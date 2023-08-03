from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import Cart
# Create your views here.
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from wishlist.models import Wishlist
from django.views.decorators.cache import cache_control
from django.http.response import JsonResponse
from products.models import Product
# from offer.models import Offer

@login_required(login_url='user_login')
def cart(request):
    if request.user.is_superuser:
                return redirect('dashboard')

    cart=Cart.objects.filter(user=request.user).order_by('id')

    total_price=0
    
    grand_total=0

    a=0
    for item in cart:
        product_price = item.product.product_price
        product_offer = item.product.offer
        brand_offer = item.product.brand.offer

        if product_offer is None and brand_offer is None:
            total_price += product_price * item.product_qty
        
            a=product_price * item.product_qty
        else:
            if product_offer and brand_offer:
                # If both product and brand have offers, choose the maximum discount
                max_discount = max(product_offer.discount_amount, brand_offer.discount_amount)
            elif product_offer:
                max_discount = product_offer.discount_amount
            else:
                max_discount = brand_offer.discount_amount

            discount = (max_discount / 100) * product_price
           
            discounted_price = product_price - discount

            total_price += discounted_price * item.product_qty
         
            a=discounted_price * item.product_qty

        grand_total = total_price
           
            
          

    context={
        'cart':cart,
        'total_price':total_price,
        'product_price':a,
        'grand_total':grand_total
    }


    return render(request,'user/cart.html',context)




@cache_control(no_cache=True,must_revalidate=True,no_store=True)


def add_cart(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
           
            prod_id = request.POST.get('prod_id')
            add_qty= int(request.POST.get('add_qty'))
            try:
                product_check = Product.objects.get(id=prod_id)
                

            except Product.DoesNotExist:
                return JsonResponse({'status': 'No such product found'})

            if Cart.objects.filter(user=request.user, product_id=prod_id).exists():
                prod_qty = int(request.POST.get('product_qty'))
                if product_check.quantity > prod_qty:
                    Cart.objects.filter(user=request.user, product_id=prod_id).update(product_qty=prod_qty + add_qty)
                    return JsonResponse({'status': 'Product quantity increased'})
                else:
                    return JsonResponse({'status': "Only few quantity available"})

            else:
                prod_qty = add_qty
                
                if product_check.quantity >= prod_qty:
                    Cart.objects.create(user=request.user, product_id=prod_id, product_qty=prod_qty)
                    # try:
                    #     if Wishlist.objects.filter(user = request.user, product = prod_id).exists():
                    #         wishlist = Wishlist.objects.filter(user = request.user, product = prod_id)
                    #         wishlist.delete()
                    # except:
                        
                    #     pass
                    return JsonResponse({'status': 'Product added successfully'})
                else:
                    return JsonResponse({'status': "Only few quantity available"})
        else:
            return JsonResponse({'status': 'Login to continue'})
    return redirect('product_detail')



# Update cart quantity
# @cache_control(no_cache=True,must_revalidate=True,no_store=True)



                   
@login_required(login_url='user_login')
def update_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        if (Cart.objects.filter(user=request.user, product_id=product_id)):
            prod_qty = request.POST.get('product_qty')
            cart = Cart.objects.get(product_id=product_id, user=request.user)

            
            single_total = cart.product.get_offer()
            cartes = cart.product.quantity
            if int(cartes) >= int(prod_qty):
                cart.product_qty = prod_qty
                cart.save()

                carts = Cart.objects.filter(user = request.user).order_by('id')
                total_price = 0
   
                # a = cart.product.get_offer() * cart.product_qty
                for item in carts:
                    product_price = item.product.product_price
                    product_offer = item.product.offer
                    brand_offer = item.product.brand.offer

                    if product_offer is None and brand_offer is None:
                        total_price += product_price * item.product_qty
                    
                       
                       
                    else:
                        if product_offer and brand_offer:
                            # If both product and brand have offers, choose the maximum discount
                            max_discount = max(product_offer.discount_amount, brand_offer.discount_amount)
                        elif product_offer:
                            max_discount = product_offer.discount_amount
                        else:
                            max_discount = brand_offer.discount_amount

                        discount = (max_discount / 100) * product_price
           
                        discounted_price = product_price - discount

                        total_price += discounted_price * item.product_qty
                     
                        
                        
                                
                return JsonResponse({'status': 'Updated successfully','sub_total':total_price,'product_price':single_total,'quantity':prod_qty})
            else:
                return JsonResponse({'status': 'Not allowed this Quantity'})
    return JsonResponse('something went wrong, reload page',safe=False)

# Deletecart
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required(login_url='user_login')
def deletecartitem(request,product_id):
    
    
    product_id = product_id
    cart_items = Cart.objects.filter(user=request.user, product=product_id)
    if cart_items.exists():
        cart_items.delete()
    return redirect('cart')
