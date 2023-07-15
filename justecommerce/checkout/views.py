from django.shortcuts import render,redirect

# Create your views here.
from cart.models import Cart
from userprofile.models import Address

from django.http import JsonResponse

from userprofile.models import Address
from django.contrib import messages
from products.models import Product
from checkout.models import Order, OrderItem

from django.shortcuts import render, redirect
import random
import razorpay
import string


def checkout(request):

    cartitems=Cart.objects.filter(user=request.user)
    total_price=0
    grand_total=0
    tax=0

    for item in cartitems:
        total_price = total_price + item.product.product_price * item.product_qty
        tax = total_price * 0.18
        grand_total = total_price + tax

    address=Address.objects.filter(user=request.user)


    context={
        'cartitems' : cartitems,
        'total_price' : total_price,
        'grand_total' : grand_total,
        'tax':tax,
        'address' : address
    }
        

    return render(request,'checkout/proceed.html',context)

# def placeorder(request):
#     if request.method == 'POST':
#         neworder = Order()
#         neworder.user = request.user
#         address_id = request.POST.get('address')
#         if address_id is None:
#             messages.error(request, 'Address fields is mandatory!')
#             return redirect('checkout')
#         address = Address.objects.get(id=address_id)
#         neworder.address = address
#         neworder.payment_mode = request.POST.get('payment_method')
#         neworder.payment_id = request.POST.get('payment_id')
#         cart = Cart.objects.filter(user=request.user)
#         cart_total_price = 0
#         tax = 0
#         for item in cart:
            
#             cart_total_price += item.product.product_price * item.product_qty
#             tax = cart_total_price * 0.18
#             cart_total_price +=tax
    

#         neworder.total_price = cart_total_price
#         trackno = random.randint(1111111, 9999999)
#         while Order.objects.filter(tracking_no=trackno).exists():
#             trackno = random.randint(1111111, 9999999)
#         neworder.tracking_no = trackno
#         neworder.save()

#         neworderitems = Cart.objects.filter(user=request.user)
#         for item in neworderitems:
#             OrderItem.objects.create(
#                 order=neworder,
#                 product=item.product,
#                 price=item.product.product_price,
#                 quantity=item.product_qty
                
#             )

#             # To decrease the product quantity from available stock
#         product = Product.objects.filter(id=item.product.id).first()
#         product.quantity = product.quantity - item.product_qty
#         product.save()
#         payment_mode = request.POST.get('payment_method')
#         if (payment_mode == "cod"):
#             Cart.objects.filter(user=request.user).delete()
#             return JsonResponse({'status' : "Yout order has been placed successfully"})

#         # Cart.objects.filter(user=request.user).delete()

#     return redirect('checkout')


def placeorder(request):
    if request.method == 'POST':
        # Retrieve the current user
        user = request.user

        # Retrieve the address ID from the form data
        address_id = request.POST.get('address')
        print(address_id,'1111111111111111')
        if address_id is None:
            messages.error(request, 'Address field is mandatory!')
            return redirect('checkout')

        # Retrieve the selected address from the database
        address = Address.objects.get(id=address_id)

        # Create a new Order instance and set its attributes
        neworder = Order(user=user, address=address)
        neworder.payment_mode = request.POST.get('payment_method')
       
        neworder.message = request.POST.get('order_note')

        # Calculate the cart total price and tax
        cart_items = Cart.objects.filter(user=user)
        cart_total_price = 0
        tax = 0
        for item in cart_items:
            cart_total_price += item.product.product_price * item.product_qty
        tax = cart_total_price * 0.18
        cart_total_price += tax

        neworder.total_price = cart_total_price

        # Generate a unique tracking number
        trackno = random.randint(1111111, 9999999)
        while Order.objects.filter(tracking_no=trackno).exists():
            trackno = random.randint(1111111, 9999999)
        neworder.tracking_no = trackno

      
        
        neworder.payment_id=generate_random_payment_id(10)
        while Order.objects.filter(payment_id=neworder.payment_id).exists():
            neworder.payment_id=generate_random_payment_id(10)

        neworder.save()

        # Create OrderItem instances for each cart item
        for item in cart_items:
            OrderItem.objects.create(
                order=neworder,
                product=item.product,
                price=item.product.product_price,
                quantity=item.product_qty
            )

            # Decrease the product quantity from the available stock
            product = Product.objects.filter(id=item.product.id).first()
            product.quantity -= item.product_qty
            product.save()

        # Delete the cart items after the order is placed
        cart_items.delete()

        payment_mode = request.POST.get('payment_method')
        if payment_mode == "cod" or payment_mode == 'razorpay':
            
            return JsonResponse({'status': "Your order has been placed successfully"})
       

    return redirect('checkout')

def generate_random_payment_id(length):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=length))




def razarypaycheck(request):
    cart = Cart.objects.filter(user=request.user)
    total_price = 0
    grand_total=0
    tax=0
    for item in cart:
  
        total_price = total_price + item.product.product_price * item.product_qty
        tax = total_price * 0.18
        grand_total += total_price+tax
    
    return JsonResponse({'total_price': total_price})






def add_checkout_address(request):
    if request.method == 'POST':
        address = Address()
        address.user = request.user
        address.first_name = request.POST.get('firstname')
        address.last_name = request.POST.get('lastname')
        address.country = request.POST.get('country')
        address.address = request.POST.get('address')
        address.city = request.POST.get('city')
        address.pincode = request.POST.get('pincode')
        address.phone = request.POST.get('phone')
        address.email = request.POST.get('email')
        address.state = request.POST.get('state')
        address.order_note = request.POST.get('ordernote')
        # address.payment_mode = request.POST.get('payment_method')
        address.save()

        return redirect('checkout')
    return redirect('checkout')