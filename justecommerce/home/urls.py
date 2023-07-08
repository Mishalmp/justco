from django.urls import path

from . import views

urlpatterns=[

    path('',views.home,name='home'),
    path('user_logout/',views.user_logout,name='user_logout'),
    path('about/',views.about,name='about'),
    path('blog/',views.blog,name='blog'),
    path('shop/',views.shop,name='shop'),
    

   
]