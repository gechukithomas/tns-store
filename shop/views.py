from django.shortcuts import render, redirect
from .models import Product, Variation
from django.db.models import Exists
from django.contrib.auth.decorators import login_required
from django.contrib import auth, messages
from orders.models import OrderItem
from.models import Review
from accounts.models import Account
from django.core.paginator import Paginator
from .models import Review
from django.contrib.sites.shortcuts import get_current_site
# Create your views here.
def shop(request, category_slug=None):
    
    url                 = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        search_key      = request.POST['search_key']
        try:
            items       = Product.objects.filter(product_name__contains=search_key, is_available=True)
            items2      = Product.objects.filter(description__icontains=search_key, is_available=True)
            items.union(items, items2).order_by('?')
        except:
            messages.error(request, 'Oops item cannot be found. please try again ')   
            return redirect(url)
    elif category_slug != None:
            items           = Product.objects.filter(category__slug=category_slug, is_available=True).order_by("?")
    else:
        items   = Product.objects.filter(is_available=True).order_by("?")

    p           = Paginator(items, 6) 
    page_number = request.GET.get('page')
    page_obj    = p.get_page(page_number)

    context = {
        'PAGE_OBJ': page_obj,
        'CATEGORY': category_slug,
    }      
    return render(request, 'shop.html', context)


def shop_subcategory(request, subcategory_slug=None, variation_slug=None):
    url                 = request.META.get("HTTP_REFERER")
    if request.method  == 'POST':
        search_key      = request.POST['search_key']
        items           = Product.objects.all().filter(subcategory__slug=subcategory_slug, description__contains=search_key, is_available=True).order_by('?') 
    elif subcategory_slug != None:
        subcategory_slug_obj = Variation.objects.filter(subcategory__slug=subcategory_slug)
        if variation_slug != None:
            print(subcategory_slug, "\n\n\n\n\n")
            items       = Product.objects.filter(subcategory__slug=subcategory_slug, variation__slug=variation_slug, is_available=True).order_by("?")
            print(items,'\n\n\n')
        else:    
            items           = Product.objects.filter(subcategory__slug=subcategory_slug, is_available=True).order_by("?")
    else:
        messages.error(request, "an error occurred")
        return redirect('shop')

    p                   = Paginator(items, 8)
    page_number         = request.GET.get('page')
    page_obj            = p.get_page(page_number)

    context = {
        'PAGE_OBJ': page_obj,
        'SUBCATEGORY': subcategory_slug,
        'SUBCATEGORY_obj': subcategory_slug_obj,
        }
    return render(request, 'shop_subcategory.html', context)


def single_product(request,category_slug=None, subcategory_slug=None, variation_slug=None, product_slug=None, product_id=None):
    # url of the current page 
    url                 = request.META.get("HTTP_REFERER")
    item                = Product.objects.get(id=product_id)
    
    if request.method == 'POST':
        
        if request.user == "AnonymousUser":
            messages.error(request, "Please login to make a review")
            return redirect(url)
        
        if request.user.is_staff:
            messages.error(request, "Sorry you are not permitted to make reviews")
            return redirect(url)
        try:
            account     = Account.objects.get(email=request.user.email)
        except:
            messages.error(request, "Please login to make a review")    
            return redirect(url)
        review_exists    = Review.objects.filter(product= item,user__email=request.user.email).exists()
        if review_exists == True:
            messages.error(request, "Sorry. You are limited to a single review")
            return redirect(url)

        review_request  = request.POST['review']
        rating_request  = request.POST['rating'] 
        product         = Product.objects.get(id=product_id)
        data            = Review()
        data.user       = account
        data.product    = product
        data.review     = review_request
        data.rating     = rating_request
        data.save()
        messages.success(request, "Your review has been submitted successfully")
        return redirect(url)
    # if user is anonymous, fetch no reviews
    user = request.user
    if  user    == 'AnonymousUser':
        review_obj      = None
    else:    
        review = Review.objects.filter(product=item).order_by("-created_date")
        p = Paginator(review, 3)
        page_number     = request.GET.get('page')
        review_obj      = p.get_page(page_number)

    try:
        in_cart = OrderItem.objects.get(request_user__email=request.user.email, product=item)
    except:
        in_cart = None
        pass
    # Fetch items from Product whose subcategory slug matches the current single product
    similar_items       = item.subcategory.slug
    similar_itemz       = Product.objects.filter(subcategory__slug=similar_items, is_available=True).order_by("-id")
    print(similar_items, "\n\n\n")
    similar_p           = Paginator(similar_itemz, 5)
    similar_page_number = request.GET.get('page')
    similar_obj         =  similar_p.get_page(similar_page_number)
  

    context = { 
        'ITEM':    item,
        'IN_CART':  in_cart, 
        'REVIEW': review_obj, 
        'USER': user, 
        'SIMILAR_PRODUCT': similar_obj, 
        } 
    
    return render(request, 'single_product.html', context)
    

    