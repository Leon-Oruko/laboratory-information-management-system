from django.urls import path
from management import views
app_name = 'management'

urlpatterns = [
    path('samples/', views.sample_list_view, name='samples'),
    path('users/',views.users,name='users'),
    path('new/', views.sample_registration_view, name='new-sample'),
    path('tasks/',views.tasks,name='manager-tasks'),
    path('history/',views.history,name='manager-history'),
    path('invoice/', views.viewInvoice, name='invoice'),

]