from django.urls import path
from . import views

urlpatterns=[
    path('sample_registration',views.sample_registration_view,name='register_sample'),
    path('sample-list/', views.sample_list_view, name='sample_list'),
]