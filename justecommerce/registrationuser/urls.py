
from django.urls import path

from . import views

urlpatterns=[

  
    path('user_signup',views.user_signup,name='user_signup'),
    path('user_login',views.user_login,name='user_login'),
    path('forgot_password',views.forgot_password,name='forgot_password'),
    path('mobile_login/',views.mobile_login,name='mobile_login'),
    
]

