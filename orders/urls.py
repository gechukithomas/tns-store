from django.urls import path
from . import views
urlpatterns  = [
    path('', views.orders, name='orders'),
    path('add_order/<int:product_id>/', views.add_order, name='add_order'),
    path('remove_order/<int:product_id>/', views.remove_order, name='remove_order'),
    
    #path('submit_order/', views.submit_request,name='submit_order'),
    path('cancel_order/<int:product_id>/', views.cancel_order, name='cancel_order'),

    #path('final_submition', views.final_submition, name='final_submition'),
]