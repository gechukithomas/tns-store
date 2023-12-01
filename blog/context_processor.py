from .models import Blog, BlogViews

from django.db.models import Count
def blog_category_count(request):
    count_tech          = Blog.objects.filter(category='technology', variation="blog").count()
    count_lifestyle     = Blog.objects.filter(category='lifestyle', variation="blog").count()
    count_fashion       = Blog.objects.filter(category='fashion', variation="blog").count()
    count_art           = Blog.objects.filter(category='art', variation="blog").count()
    count_food          = Blog.objects.filter(category='food', variation="blog").count()
    count_adventure     = Blog.objects.filter(category='travel',variation="blog").count()
    context     = {
        'TECHNOLOGY': count_tech,
        'LIFESTYLE': count_lifestyle,
        'FASHION':  count_fashion,
        'ART': count_art,
        'FOOD': count_food,
        'ADVENTURE': count_adventure,
    }
    return context


def popular_blogs(request):
    popular_blogs = Blog.objects.all().order_by('?')[0:4]

    context = {
        'POPULAR_BLOGS': popular_blogs,
    }
    return context  