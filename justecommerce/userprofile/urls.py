from django.urls import path
from .import views
urlpatterns = [
    path('', views.user_profile, name='user_profile'),
    path('user_orders/', views.user_orders, name='user_orders'),
    path('addaddress/', views.add_address, name='addaddress'),
    path('editprofiles/', views.editprofile, name='editprofiles'),
    path('changepassword/', views.changepassword, name='changepassword'),
    path('deleteaddress/<int:delete_id>', views.deleteaddress, name='deleteaddress'),

]
