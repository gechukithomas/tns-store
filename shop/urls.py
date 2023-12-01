from django.urls import path
from . import views

urlpatterns = [
    path('',views.shop, name="shop"),
    path('<slug:category_slug>/', views.shop, name='shop_category'),
    path('<slug:category_slug>/srt/<slug:sort_slug>/', views.shop, name="shop_sort"),
    path('gnr/<slug:category_slug>/<slug:gender_slug>/', views.shop, name="shop_gender"),

    path('query/', views.shop, name='search'),

    #path('<slug:category_slug>/', views.shop_category, name='shop_category'),
    #path('subcategory/<slug:subcategory_slug>/', views.shop, name='shop_subcategory'),
    path('tns/<slug:subcategory_slug>/',views.shop_subcategory, name='shop_sub_subcategory'),
    #path('casduy!DFGJ/<slug:sort_slug>/', views.shop_subcategory, name='shop_sub_search'),
    path('tns/<slug:subcategory_slug>/<str:variation_slug>/', views.shop_subcategory, name='shop_sub_variation'),
    path('tns/query?/', views.shop_subcategory, name='search_shop_subcategory'),

    path('su/<slug:category_slug>/<slug:subcategory_slug>/<slug:variation_slug>/<slug:product_slug>/<int:product_id>/', views.single_product, name='single_product'),    
    #path('/owner_items/<slug:subcategory_slug>/<slug:product_slug>/<int:product_id>/', views.single_product, name='single_product'),
    path('reviews/<int:product_id>/', views.single_product, name='submit_review'),

]