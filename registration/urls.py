from django.urls import path
from . import views
app_name = 'registration'

urlpatterns=[
    path('new/',views.sample_registration_view,name='new'),
    path('samples/', views.sample_list_view, name='samples'),
]