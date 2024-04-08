from django.urls import path
from . import views

app_name = 'recommedation'


urlpatterns = [
    path('samples/', views.sample_list_view, name='samples'),
    path('recommend/', views.recommend, name='recommend'),
    path('history/', views.history, name='history'),
]