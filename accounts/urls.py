from django.urls import path
from .import views
urlpatterns = [
    path('register/', views.register, name='register'),

    path('login/', views.login, name='login'),

    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/profile/', views.edit_profile, name='edit_profile'),
    path('dashboard/recieved_orders', views.recieved_orders, name='recieved_orders'),
    path('dashboard/items_pending', views.view_items, name="pending_delivery"),
    path('dashboard/my_blogs', views.my_blogs, name='my_blogs'),
    
    path('logout/', views.logout, name='logout'),

    path('forgotpassword/', views.forgotpassword, name='forgot_password'),
    path('activate/<uidb64>/<token>/', views.activate_account, name='activate'),
    path('password_validate/<uidb64>/<token>/', views.validate_password_reset, name='reset_password_validate'),
    path('reset_password/', views.reset_password, name='reset_password'),
]