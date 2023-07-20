from django.shortcuts import render,redirect
from cart.models import Cart
from userprofile.models import Address,Wallet
from checkout.models import Order,OrderItem
from django.http import JsonResponse
from django.contrib import messages
# Create your views here.
from products.models import Product
from .models import Orderreturn

# ...................admin section.............
def admin_orders(request):
    orders=Order.objects.all().order_by('-created_at')
    order_item=OrderItem.objects.all()
    context={
        'orders':orders,
        'order_item':order_item
    }
    return render (request,'order/ad-orders.html',context)

def ad_order_detail(request,order_id):

    order_id=order_id

    od_details=Order.objects.get(id=order_id)
    order_item=OrderItem.objects.filter(order=order_id)
    ord=Order.objects.select_related('address').get(id=order_id)

    

    context={
        'order':od_details,
        'address':ord.address,
        'order_item':order_item
        
    }
    return render(request,'order/ad-order-det.html',context)

def ordercancel(request):
    orderid = int(request.POST.get('order_id'))
    orderitem_id = request.POST.get('orderitem_id')
    orderitem = OrderItem.objects.filter(id=orderitem_id).first()
    

    
    order = Order.objects.filter(id=orderid).first()
    qty = orderitem.quantity
    pid = orderitem.product.id
    product = Product.objects.filter(id=pid).first()
    

    if order.payment_mode == 'Razorpay' or order.payment_mode == 'wallet' :
        order = Order.objects.get(id=orderid)
        total_price = order.total_price

        try:
            wallet = Wallet.objects.get(user=request.user)
            wallet.wallet += total_price
            wallet.save()
        except Wallet.DoesNotExist:
            wallet = Wallet.objects.create(user=request.user, wallet=total_price)
    # Update the product quantity
    product.quantity = product.quantity + qty
    product.save()
    orderitem.quantity = 0
    orderitem.status = 'Cancelled'
    orderitem.save()
    return redirect('user_profile')

def orderreturn(request,return_id):
    if request.method == 'POST':
        print(return_id,'rrrrrrrrrrrrrrrrrrrrrrrrrrr')
        options = request.POST.get('options')
        reason = request.POST.get('reason')
# validation
        if options.strip() == '':
            messages.error(request, "enter valid Options")
            return redirect('vieworderdetail')
        try:
            orderitem_id = OrderItem.objects.get(id=return_id)
        except OrderItem.DoesNotExist:
            return redirect('user_profile')
        qty = orderitem_id.quantity
        pid = orderitem_id.product.id
        order_id = Order.objects.get(id = orderitem_id.order.id)
        
        product = Product.objects.filter(id=pid).first()
        product.quantity = product.quantity + qty
        product.save()
        orderitem_id.status = 'Return'
        total_p = orderitem_id.price
        print(total_p)
        orderitem_id.save()
        returnorder = Orderreturn.objects.create(user = request.user, order = order_id, options=options, reason=reason)
        try:
            wallet = Wallet.objects.get(user=request.user)
            wallet.wallet += total_p
            wallet.save()
        except Wallet.DoesNotExist:
            wallet = Wallet.objects.create(user=request.user, wallet=total_p)
        orderitem_id.quantity = 0
        orderitem_id.price = 0
        orderitem_id.save()
        return redirect('user_profile')




def changestatus(request):
    if not request.user.is_superuser:
        return redirect('admin_login')
    orderitem_id = request.POST.get('orderitem_id')
    order_status = request.POST.get('order_status')
    orderitems = OrderItem.objects.get(id = orderitem_id)

    orderitems.status = order_status
    orderitems.save()
    return JsonResponse({'status': "Updated"+ str(order_status) + "successfully"}) 

def change_od_status(request):
    if not request.user.is_superuser:
        return redirect('admin_login')
    order_id = request.POST.get('order_id')

    order_status = request.POST.get('order_od_status')
    print(order_id,order_status,'1111111111')
    try:
        order = Order.objects.get(id=order_id)
        order.od_status = order_status
        order.save()
    # The order's od_status field has been updated
    except Order.DoesNotExist:
    # Handle the case where the order does not exist
        print("Order does not exist.")
    return JsonResponse({'status': "Updated"+ str(order_status) + "successfully"})


# ..................user section....................



