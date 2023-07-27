from django.urls import path

from . import views

urlpatterns=[

    path('',views.home,name='home'),
    path('user_logout/',views.user_logout,name='user_logout'),
    path('about/',views.about,name='about'),
    path('contact/',views.contact,name='contact'),
    path('shop/',views.shop,name='shop'),
    

   
]