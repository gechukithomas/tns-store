from shop.models import Category
from shop.models import Subcategory

def category_links(request):
    links       = Category.objects.all()
    return dict(links_category=links)

def subcategory_fashion_links(request):
    links       = Subcategory.objects.filter(category__slug='fashion')
    return dict(links_fashion=links)

def subcategory_electronics_links(request):
    links       = Subcategory.objects.filter(category__slug='electronics')
    return dict(links_electronics=links)

def subcategory_furniture_links(request):
    links       = Subcategory.objects.filter(category__slug='furniture')
    return dict(links_furnitures=links)

def user_subcategory_page(request, category):
    category  = category,
    return dict(CAT=category)

    