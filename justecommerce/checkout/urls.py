from django.urls import path
from .import views
urlpatterns = [
    path('checkout/',views.checkout,name='checkout'),
    path('add_checkout_address/',views.add_checkout_address,name='add_checkout_address'),
    path('edit_check_address/<int:edit_id>',views.edit_check_address,name='edit_check_address'),
    path('placeorder/',views.placeorder,name='placeorder'),
    path('proceedtopay/',views.razarypaycheck,name='razarypaycheck'),
    path('apply_coupon/',views.apply_coupon,name='apply_coupon'),
    # path('update_grand_total/', views.update_grand_total, name='update_grand_total'),
    path('remove_coupon/', views.remove_coupon, name='remove_coupon'),
    path('cancel_order_before/', views.cancel_order_before, name='cancel_order_before'),
    path('deletebuyitem/<int:product_id>', views.deletebuyitem, name='deletebuyitem'),

    
    path('buynow_checkout/', views.buynow_checkout, name='buynow_checkout'),
    path('razarybuynow_paycheck/', views.razarybuynow_paycheck, name='razarybuynow_paycheck'),
    path('buynow_placeorder/', views.buynow_placeorder, name='buynow_placeorder'),
    path('add_buy_checkout_address/', views.add_buy_checkout_address, name='add_buy_checkout_address'),
    path('cancel_buy_before/', views.cancel_buy_before, name='cancel_buy_before'),
    path('apply_buy_coupon/',views.apply_buy_coupon,name='apply_buy_coupon'),
    path('edit_buy_address/<int:edit_id>',views.edit_buy_address,name='edit_buy_address'),


    

]




