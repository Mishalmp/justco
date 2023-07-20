from django.contrib import admin

from .models import Coupon,CouponUsage
# Register your models here.
admin.site.register(CouponUsage)
admin.site.register(Coupon)
