from django.urls import path
from django.contrib.auth import views as auth_views
from. import views
app_name = 'login'

urlpatterns=[
    path('accounts/login/',views.user_login,name='login'),
     path('accounts/logout/', views.user_logout, name='logout'),
    path('register',views.user_register,name='register')
]