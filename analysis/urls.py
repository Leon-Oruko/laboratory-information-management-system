from django.urls import path
from . import views
app_name = 'analysis'

urlpatterns = [
    path('sample-list/', views.sample_list_view, name='sample-list-view'),
    path('analyse/', views.picked_samples, name='analyse'),
    path('history/', views.past_analysis, name='history'),
    path('analyse/<path:sample_id>/', views.analyse_task, name='analyse_task'),

    # ... other url patterns ...
]




