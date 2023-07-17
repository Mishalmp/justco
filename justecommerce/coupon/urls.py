from django.urls import path
from .import views
urlpatterns = [
   
   path('coupons/',views.coupons,name='coupons'),
   path('addcoupon/',views.addcoupon,name='addcoupon'),
   path('editcoupon/<int:coupon_id>',views.editcoupon,name='editcoupon'),
   path('deletecoupon/<int:coupon_id>',views.deletecoupon,name='deletecoupon'),

]