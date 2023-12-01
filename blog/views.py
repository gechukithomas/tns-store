from django.shortcuts import render, redirect
from .models import Blog, BlogViews, BlogComment
from django.contrib import messages
from django.core.paginator import Paginator
from accounts.models import Account, UserProfile
from django.contrib.auth.decorators import login_required
from.forms import AddBlogForm
import random
# Create your views here.
def blog(request, blog_category=None, owner=None, service=None):
    print(service, "\n\n\n\n")
    url                 = request.META.get("HTTP_REFERER")
    blog                = Blog.objects.all().order_by('-date_added')
    if request.method == 'POST':
        text        = request.POST['search_key']
        if text == None:
            blog        = Blog.objects.all().order_by('-id')
        else:
            blog        = Blog.objects.filter(title__icontains=text)
            blog2       = Blog.objects.filter(short_description__icontains=text)
            blog = blog.union(blog, blog2).order_by("id")

            if blog == None:
                blog    = Blog.objects.all().order_by('-id')
                messages.error(request, "Blog with the description you requested for do not exist")
                return redirect(url)
    elif blog_category != None:            
        blog    = Blog.objects.filter(category=blog_category, variation='blog').order_by('-id')
        if blog == None:
            blog = Blog.objects.all().order_by('-id')
            messages.error(request, "Blog not found")   
    elif owner != None:
        print("Entered owner if control\n\n\n\n\n")
        blog_author     = Account.objects.get(username=owner)
        blog    = Blog.objects.filter(author=blog_author)
    elif service != None:
        variaion_x =  "service"
        blog    = Blog.objects.filter(variation=variaion_x).order_by("-id")
    else:
        blog    = Blog.objects.filter(variation="blog").order_by("-id")

    p = Paginator(blog, 6)
    page_number = request.GET.get('page')
    blog_object  = p.get_page(page_number)

    if request.user.is_authenticated == True:
        count_staff_members     = Account.objects.filter(is_staff=True).count()
        xy  = random.randint(1, count_staff_members)
        try:
            get_a_single_staff_user_from_account_model = Account.objects.get(id=xy)
        except: 
            get_a_single_staff_user_from_account_model = Account.objects.get(id=1)

        user_prof   = UserProfile.objects.get(user=get_a_single_staff_user_from_account_model)
    else:
        admin_account   = Account.objects.get(id=1)
        user_prof = UserProfile.objects.get(user=admin_account) 
    context     = {
        'BLOG': blog_object,
        'USER': user_prof,
    }

    return render(request,'blog/blog.html', context)

@login_required(login_url='login')
def single_blog(request, category=None, blog=None, blog_id=None):
    account             = Account.objects.get(email=request.user.email)
    url                 = request.META.get("HTTP_REFERER")
    if request.method == 'POST':
        comment                 = request.POST['comment']
        request_blog_id         = request.POST['ID']

        new_blog                = Blog.objects.get(id=request_blog_id)
        max_comments            = BlogComment.objects.filter(comment_user=account, blog=new_blog).count()
        if max_comments > 1:
            messages.error(request, 'Sorry! You are limited to two comments on a post')
            return redirect(url)
        # request id of the blog from the  input field(hidden html attribute)
        dx                  = BlogComment()
        dx.comment_user     = account
        dx.blog             = new_blog
        dx.comment          = comment
        dx.save()
        messages.success(request, "Comment successfully added")
        return redirect(url)
    
    blog                = Blog.objects.get(id=blog_id)
   
    if account.email == request.user.email:
        blog_form   = AddBlogForm(request.POST, request.FILES, instance=account)
        
    userviewed = BlogViews.objects.filter(viewed_user=request.user.email, blog=blog).exists()
    if userviewed != True:
        data                = BlogViews()
        data.viewed_user    = request.user.email
        data.blog           = blog
        data.views          =+ 1 
        data.save()
    else:
        pass
  
    blog_comments   = BlogComment.objects.filter(blog=blog)

    blog_comments_p              = Paginator(blog_comments, 3)
    blog_comments_page_number    = request.GET.get('page')
    blog_comments_object         = blog_comments_p.get_page(blog_comments_page_number)

    request_blog_profile = UserProfile.objects.get(user=account)
    context = {
        'BLOG':blog,
        'BLOGCOMMENT': blog_comments_object,
    }
    return render(request, 'blog/single_blog.html', context)    
@login_required(login_url='login')
def add_blog(request):
    account     = Account.objects.get(email=request.user.email)
    url         = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        form            = AddBlogForm(request.POST, request.FILES) 

        category        = request.POST['category']
        variation       = request.POST['variation']
        title           = request.POST['title']
        short_description = request.POST['short_description']
        description         = request.POST['description']
        image               = request.FILES['image']

        data            = Blog()
        data.author     = account
        data.category   = category
        data.variation  = variation
        data.title      = title
        data.short_description  = short_description
        data.description        = description
        data.image              =  image
        data.save()
        messages.success(request, 'Your blog post has been uploaded succesfully')
        return redirect('blog')
    else:
        form    =   AddBlogForm()
    context = {
        'form': form
    }    
    return render(request, 'blog/add_blog.html', context)

 

