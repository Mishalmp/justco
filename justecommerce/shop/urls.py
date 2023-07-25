
from django.urls import path

from .views import *

urlpatterns=[

  
    path('product_detail/<slug:product_id>',product_detail,name='product_detail'),
    path('add_buynow/',add_buynow,name='add_buynow'),
  
    
]
