from django.urls import path
from .import views
urlpatterns = [
    path('checkout/',views.checkout,name='checkout'),
    path('add_checkout_address/',views.add_checkout_address,name='add_checkout_address'),
    path('placeorder/',views.placeorder,name='placeorder'),
    path('proceedtopay/',views.razarypaycheck,name='razarypaycheck'),
    path('apply_coupon/',views.apply_coupon,name='apply_coupon'),
    # path('update_grand_total/', views.update_grand_total, name='update_grand_total'),
    path('remove_coupon/', views.remove_coupon, name='remove_coupon'),
    path('cancel_order_before/', views.cancel_order_before, name='cancel_order_before'),

    
    path('buynow_checkout/', views.buynow_checkout, name='buynow_checkout'),
    path('razarybuynow_paycheck/', views.razarybuynow_paycheck, name='razarybuynow_paycheck'),
    path('buynow_placeorder/', views.buynow_placeorder, name='buynow_placeorder'),
    path('add_buy_checkout_address/', views.add_buy_checkout_address, name='add_buy_checkout_address'),
    path('cancel_buy_before/', views.cancel_buy_before, name='cancel_buy_before'),
    

]




