from django.urls import path
from .import views
urlpatterns = [
 
 path('orders/',views.admin_orders,name='admin_orders'),
 path('ad_order_detail/<int:order_id>',views.ad_order_detail,name='ad_order_detail'),
 path('changestatus/',views.changestatus,name='changestatus'),
 path('change_od_status/',views.change_od_status,name='change_od_status')


]