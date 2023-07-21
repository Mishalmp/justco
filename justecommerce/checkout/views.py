from django.shortcuts import render,redirect
from django.template.loader import render_to_string
# Create your views here.
from cart.models import Cart
from userprofile.models import Address
from xhtml2pdf import pisa
from django.http import JsonResponse

from userprofile.models import Address
from django.contrib import messages
from products.models import Product
from checkout.models import Order, OrderItem
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
import random
import razorpay
import string
from coupon.models import Coupon,CouponUsage
from userprofile.models import Wallet
from django.contrib.auth.models import User
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
import os
from django.http import HttpResponse

def checkout(request):
    cartitems = Cart.objects.filter(user=request.user)
    total_price = 0

    for item in cartitems:
        if item.product.offer is None:
            total_price += item.product.product_price * item.product_qty
        else:
            total_price += item.product.product_price * item.product_qty
            total_price -= item.product.offer.discount_amount

    coupons = Coupon.objects.filter(is_active=True)
    applied_coupon = None
    grand_total = total_price

    if request.method == 'POST':
        coupon_code = request.POST.get('coupon_code')
        if coupon_code:
            try:
                applied_coupon = Coupon.objects.get(coupon_code=coupon_code, is_active=True)
                grand_total = total_price - (total_price * (applied_coupon.discount / 100))
            except Coupon.DoesNotExist:
                pass

    address = Address.objects.filter(user=request.user)

    context = {
        'cartitems': cartitems,
        'total_price': total_price,
        'grand_total': grand_total,
        'applied_coupon': applied_coupon,
        'address': address,
        'coupons': coupons,
        'CouponUsage': CouponUsage.objects.filter(user=request.user).last()
    }

    return render(request, 'checkout/proceed.html', context)



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

def cancel_order_before(request):

    return redirect('cart')
    


def placeorder(request):
    if request.method == 'POST':
        # Retrieve the current user
        user = request.user
        usr=User.objects.get(username=request.user)
        # Retrieve the address ID from the form data
        address_id = request.POST.get('address')
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
        
        for item in cart_items:
            if item.product.offer == None:
                cart_total_price += item.product.product_price * item.product_qty
                
                
            else:
                cart_total_price += item.product.product_price * item.product_qty
                cart_total_price -= item.product.offer.discount_amount

        payment_mode = request.POST.get('payment_method')
        if (payment_mode == "wallet"):
            try:
                wallet = Wallet.objects.get(user=request.user)
            except Wallet.DoesNotExist:
                wallet = Wallet.objects.create(user=request.user, wallet=0)

            if wallet.wallet >= cart_total_price:
                wallet.wallet = wallet.wallet - cart_total_price
                wallet.save()
            else:
                return JsonResponse({'status': "Your wallet amount is very low"})
        # Check if a coupon is applied
        coupon = CouponUsage.objects.filter(user=user, used=True).first()
        if coupon:
            # Calculate the discounted price if a coupon is applied
            discount = cart_total_price * (coupon.coupon.discount / 100)
            cart_total_price -= discount

        neworder.total_price = cart_total_price

        # Generate a unique tracking number
        trackno = random.randint(1111111, 9999999)
        while Order.objects.filter(tracking_no=trackno).exists():
            trackno = random.randint(1111111, 9999999)
        neworder.tracking_no = trackno

        neworder.payment_id = generate_random_payment_id(10)
        while Order.objects.filter(payment_id=neworder.payment_id).exists():
            neworder.payment_id = generate_random_payment_id(10)

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
        if payment_mode == "cod" or payment_mode == 'razorpay' or payment_mode == 'wallet':
            

            generate_invoice_pdf(request, neworder.id)
            return JsonResponse({'status': "Your order has been placed successfully"})
        
        

    return redirect('checkout')

def generate_invoice_pdf(request, order_id):
    try:
        order = Order.objects.get(id=order_id)  # Use get() instead of filter()
        order_items = OrderItem.objects.filter(order=order)
    except Order.DoesNotExist:
        # Handle the case if the order does not exist
        return HttpResponse("Order not found", status=404)

    # Render the XHTML template with dynamic data
    context = {
        'order': order,
        'order_items': order_items,
    }
    rendered_template = render_to_string('order/invoice_template.html', context)

    # Convert the XHTML content to PDF
    pdf_file = os.path.join(settings.BASE_DIR, 'invoice.pdf')
    with open(pdf_file, 'wb') as pdf:
        pisa.CreatePDF(rendered_template, dest=pdf)

    # Send the email with both the PDF attachment and the order confirmation
    subject = "Welcome to Just Watches, Order Placed!!!"
    message = f'''
        Your order has been placed successfully.
        Hello {order.user.username},
        Your Order has been placed successfully.
        Thank you for choosing JUST Watches!
        Payment mode: {order.payment_mode}
        Your Payment ID is {order.payment_id}
        Your Order Tracking ID: {order.tracking_no}
        Expected Delivery Date: {order.expected_delivery}
    '''
    from_email = settings.EMAIL_HOST_USER
    to_email = [order.user.email]

    email = EmailMessage(subject, message, from_email, to_email)
    email.attach_file(pdf_file)  # Attach the PDF to the email
    email.send()

    # Delete the temporary PDF file
    os.remove(pdf_file)
    return redirect('placeorder')




def apply_coupon(request):
    if request.method == 'POST':
        coupon_code = request.POST.get('coupon_code')
        grand_total = float(request.POST.get('grand_total', 0))  # Convert to float
        print(grand_total, 'oooooooooooooooooooooooooooooo')
        
        if coupon_code.strip() == '':
            return JsonResponse({'status': 'Field is blank'})
        
        if coupon_code == 'No Coupon Applied':
            return JsonResponse({'status': 'No Coupon Applied'})
        
        try:
            coupon = Coupon.objects.get(coupon_code=coupon_code, is_active=True)
        except Coupon.DoesNotExist:
            return JsonResponse({'status': 'Coupon does not exist'})

        # Check if the user has already used the coupon
        existing_coupon_usage = CouponUsage.objects.filter(user=request.user, coupon=coupon)
        if existing_coupon_usage.exists():
            existing_coupon_usage = existing_coupon_usage.first()
            # Remove the discount of the existing coupon from the grand_total
            grand_total += (grand_total * (existing_coupon_usage.coupon.discount / 100))
            existing_coupon_usage.delete()

        if grand_total > coupon.min_price:
            coupon_discount = coupon.discount
            grand_total = grand_total - (grand_total * (coupon.discount / 100))
            usercoupon = CouponUsage.objects.create(user=request.user, coupon=coupon, used=True, total_price=grand_total)
            usercoupon.save()
            return JsonResponse({
                'status': 'Coupon added successfully',
                'coupon_discount': coupon_discount,
                'grand_total': grand_total,
            })
        else:
            return JsonResponse({'status': 'You are not eligible for this coupon'})
            
    return JsonResponse({'status': 'Invalid request'})

# def update_grand_total(request):
#     if request.method == 'POST':
#         grand_total = request.POST.get('grand_total')
#         request.session['grand_total'] = grand_total
#         return JsonResponse({'status': 'Grand total updated successfully'})
#     return JsonResponse({'status': 'Invalid request'})

def remove_coupon(request):
    if request.method == 'POST':
        coupon_code = request.POST.get('coupon_code')

        if coupon_code.strip() == '':
            return JsonResponse({'status': 'Field is blank'})

        if coupon_code == 'No Coupon Applied':
            return JsonResponse({'status': 'No Coupon Applied'})

        try:
            coupon = get_object_or_404(Coupon, coupon_code=coupon_code, is_active=True)
        except Coupon.DoesNotExist:
            return JsonResponse({'status': 'Coupon does not exist'})

        existing_coupon_usage = CouponUsage.objects.filter(user=request.user, coupon=coupon)
        if existing_coupon_usage.exists():
            existing_coupon_usage = existing_coupon_usage.first()
            grand_total = float(request.POST.get('grand_total', 0))
            # Add the discount of the existing coupon back to the grand_total
            grand_total += (grand_total * (existing_coupon_usage.coupon.discount / 100))
            existing_coupon_usage.delete()

            return JsonResponse({
                'status': 'Coupon removed successfully',
                'grand_total': grand_total,
            })
        else:
            return JsonResponse({'status': 'Coupon is not applied'})

    return JsonResponse({'status': 'Invalid request'})
# def apply_coupon(request):
#     coupon_code = request.POST.get('coupon_code')
#     user = request.user
    
#     try:
#         coupon = Coupon.objects.get(coupon_code=coupon_code, is_active=True)
        
#         # Retrieve the existing orders based on user
#         orders = Order.objects.filter(user=user)
        
#         # Apply the coupon discount to each order
#         for order in orders:
#             order.total_price -= (order.total_price * (coupon.discount / 100))
#             order.coupon = coupon
#             order.save()

#         return JsonResponse({'success': True})

#     except Coupon.DoesNotExist:
#         return JsonResponse({'success': False, 'error': 'Invalid coupon code'})

#     except Order.DoesNotExist:
#         return JsonResponse({'success': False, 'error': 'Order does not exist'})

#     except Exception as e:
#         return JsonResponse({'success': False, 'error': str(e)})





def generate_random_payment_id(length):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=length))




def razarypaycheck(request):
    cart = Cart.objects.filter(user=request.user)
    total_price = 0
    grand_total=0
    
    for item in cart:
        if item.product.offer == None:
            total_price = total_price + item.product.product_price * item.product_qty
            
            grand_total += total_price
        else:
            total_price += item.product.product_price * item.product_qty
            total_price -= item.product.offer.discount_amount
            
            
    
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