from django.urls import path
from . import views
urlpatterns = [
    path('client_delete/<int:product_id>/', views.delete_order, name='client_delete_order'),
]