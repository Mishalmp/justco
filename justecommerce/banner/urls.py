from django.urls import path

from .views import *

urlpatterns=[

    path('banners/', banners, name='banners'),
    
    path('createbanners/', createbanners, name='createbanners'),
    path('editbanner/<int:editbanner_id>', editbanner, name='editbanner'),
    path('deletebanner/<int:deletebanner_id>',deletebanner, name='deletebanner'),
   



]
