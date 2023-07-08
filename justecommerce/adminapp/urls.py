from django.urls import path

from .views import *

urlpatterns=[

    path('admin_login/',admin_login,name='admin_login'),
    path('admin_signup/',admin_signup,name='admin_signup'),
    path('',dashboard,name='dashboard'),
    path('admin_logout/',admin_logout,name='admin_logout'),
    path('user/',user, name='user'),
    path('user/blockuser/<int:user_id>',blockuser, name='blockuser'),
    path('user/searchuser/',searchuser, name='searchuser')
   



]
