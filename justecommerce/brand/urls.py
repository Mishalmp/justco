

from django.urls import path

from .views import *

urlpatterns=[

 path('brands/', brands, name='brands'),
    path('search_brand/',search_brand, name='search_brand'),
    path('createbrands/', createbrands, name='createbrands'),
    path('editbrands/<slug:editbrands_id>', editbrands, name='editbrands'),
    path('deletebrands/<slug:deletebrands_id>',deletebrands, name='deletebrands'),
   



]






