from django.shortcuts import render,redirect
from .models import Coupon,CouponUsage
from django.contrib import messages
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required

# Create your views here.



@login_required(login_url='admin_login')
def coupons(request):
    if not request.user.is_superuser:
        return redirect('admin_login')
    
    coupons=Coupon.objects.all()
    context={
        'coupons':coupons
    }
    return render(request,'coupon/coupon.html',context)





def addcoupon(request):
    if not request.user.is_superuser:
        return redirect('admin_login')
    if request.method == 'POST':
        coupon = request.POST.get('coupon')
        coupon_code = request.POST.get('coupon_code')
        discount = request.POST.get('discount')
        min_price = request.POST.get('min_price')
        valid_from = request.POST.get('valid_from')
        valid_to = request.POST.get('valid_to')

        try:
            is_active = request.POST.get('is_active',False)
            if is_active == 'on':
                is_active = True
            else:
                is_active = False
        except:
            is_active = False
        if Coupon.objects.filter(coupon=coupon).exists():
            messages.error(request, 'coupon already exists')
            return redirect('coupons')
        if Coupon.objects.filter(coupon_code=coupon_code).exists():
            messages.error(request, 'coupon code already exists')
            return redirect('coupons')
        coupon = Coupon(
            coupon=coupon,
            coupon_code=coupon_code,
            discount=discount,
            min_price=min_price,
            valid_from=valid_from,
            valid_to=valid_to,
            is_active=is_active
        )
        coupon.save()
        return redirect('coupons')
    
def editcoupon(request,coupon_id):
   
    if not request.user.is_superuser:
        return redirect('admin_login')

    coupon = Coupon.objects.get(id=coupon_id)

    if request.method == 'POST':
        coupon_name = request.POST.get('coupon')
        coupon_code = request.POST.get('coupon_code')
        discount = request.POST.get('discount')
        min_price = request.POST.get('min_price')
        valid_from = request.POST.get('valid_from')
        valid_to = request.POST.get('valid_to')
        
        try:
            is_active = request.POST.get('is_active', False)
            is_active = bool(is_active)
        except:
            is_active = False
        
        if Coupon.objects.filter(coupon=coupon_name).exclude(id=coupon_id).exists():
            messages.error(request, 'Coupon name already exists')
            return redirect('coupons')
        
        if Coupon.objects.filter(coupon_code=coupon_code).exclude(id=coupon_id).exists():
            messages.error(request, 'Coupon code already exists')
            return redirect('coupons')

        coupon.coupon = coupon_name
        coupon.coupon_code = coupon_code
        coupon.discount = discount
        coupon.min_price = min_price
        coupon.valid_from = valid_from
        coupon.valid_to = valid_to
        coupon.is_active = is_active

        coupon.save()
        return redirect('coupons')


def deletecoupon(request,coupon_id):
    if not request.user.is_superuser:
        return redirect('admin_login')
    
    coupon=Coupon.objects.get(id=coupon_id)
    coupon.delete()
    return redirect('coupons')
