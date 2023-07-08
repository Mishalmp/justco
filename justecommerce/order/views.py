from django.shortcuts import render,redirect
from cart.models import Cart
from userprofile.models import Address
from checkout.models import Order,OrderItem
from django.http import JsonResponse
# Create your views here.


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