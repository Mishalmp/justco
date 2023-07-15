from django.urls import path
from .import views
urlpatterns = [
    path('', views.user_profile, name='user_profile'),
    
    path('add_address/', views.add_address, name='add_address'),
    path('editprofile/', views.editprofile, name='editprofile'),
    path('changepassword/', views.changepassword, name='changepassword'),
    path('deleteaddress/<int:delete_id>', views.deleteaddress, name='deleteaddress'),
    path('edit_address/<int:edit_id>', views.edit_address, name='edit_address'),
    # path('get_order', views.get_order, name='get_order'),

]
