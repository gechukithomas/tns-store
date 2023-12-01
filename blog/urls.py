from django.urls import path
from .import views
urlpatterns = [
    path('',views.blog, name='blog'),
    path('cls/<str:blog_category>/', views.blog, name='blog_category'),
    path('tns/<slug:service>/', views.blog, name='blog_service'),
    path('auth/<slug:owner>/',views.blog, name='blog_owner'),
    path('search/', views.blog, name='blog_search'),
   
    path('<str:category>/<str:blog>/<int:blog_id>/', views.single_blog, name='single_blog'),
    
    path('submit_comment/', views.single_blog , name='submit_blog_comment'),    

    path('add_blog/', views.add_blog, name='add_blog'),
]