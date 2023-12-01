from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegistrationForm, UserProfileForm, UserForm
from .models import Account, UserProfile
from django.contrib import messages, auth
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.http import HttpResponse
from django.conf import settings
import datetime
from orders.models import OrderItem, delivered_items
from blog.models import Blog
from django.core.paginator import Paginator
# Create your views here.
def register(request):
    if request.method == 'POST':
        form                = RegistrationForm(request.POST)
        if form.is_valid():

            first_name      = form.cleaned_data['first_name']
            last_name       = form.cleaned_data['last_name']
            phone_number    = form.cleaned_data['phone_number']
            email           = form.cleaned_data['email']
            password        = form.cleaned_data['password']

            username        = email.split('@')[0]

            
            user            = Account.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
            user.phone_number   = phone_number
            user.is_active = False
            user.save()
            
            
            current_site  = get_current_site(request)
        
            subject = 'Please activate your account'
            
            message = render_to_string('accounts/account_verification.html',{
                'user':     user,
                'domain':   current_site,
                'uid':      urlsafe_base64_encode(force_bytes(user.pk)),
                'token':    default_token_generator.make_token(user), 
            })
            print(message)
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email]

            new_subject = "New registered user"
            new_message = "Hello Sir\nA new user having an email of {} has requested for an account registration on Tns Stores".format(email)
            new_recipient_list = ['optimarsalmefranchise@gmail.com']
        
            send_mail(subject, message, email_from, recipient_list, fail_silently=True)
            send_mail(new_subject, new_message, email_from, new_recipient_list, fail_silently=True)
            messages.success(request, 'Hello {0}, thank you for registering with TnS Stores\nPlease check your mail to confirm your account.'.format(username))
            return redirect ('login')
    else:
        form        = RegistrationForm()


    context     = {
        'form':     form
    } 
    return render(request, 'accounts/register.html', context)              


def activate_account(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account.objects.get(pk=uid)
    except(Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True 
        user.save()
        s = UserProfile()
        s.user = user
        s.bio_description = 'Cool person'
        s.address_line_1 = 'Kitengela'
        s.address_line_2 = 'Kitengela'
        s.save()
        messages.success(request, "Congratulations. Your account has been verified successfully")  
        return redirect('login')          
    else:
        messages.error(request, "Invalid activation link")   
        return redirect('register') 
@login_required(login_url='login')
def dashboard(request, total=0, quantity=0, order_items=None):
    account = Account.objects.get(email=request.user.email)
    if account.is_staff == True:
        order_items =   OrderItem.objects.filter(product__owner=account).order_by('-id')
        for order_item in order_items:
            total += (order_item.product.price * order_item.quantity)
            quantity += order_item.quantity
    else:   
        try:
            order_items    = OrderItem.objects.filter(request_user=account)
            for order_item in order_items:
                total += (order_item.product.price * order_item.quantity)
                quantity += order_item.quantity
       
        except:
            pass
    userprofile = UserProfile.objects.get(user=account)
    context     = {
        'TOTAL':    total,
        'QUANTITY':     quantity,
        'ORDER_ITEM':      order_items,
        'ACCOUNT':      userprofile,
    }

    return render(request, 'dashboard/dashboard.html', context)

  
def edit_profile(request):
    userprofile = get_object_or_404(UserProfile, user=request.user)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=userprofile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated')
            return redirect('edit_profile')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=userprofile)
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }    
    return render(request, 'dashboard/edit_profile.html',context)
@login_required(login_url='login')
def recieved_orders(request):
    account     = Account.objects.get(email=request.user.email)
    orders      = delivered_items.objects.filter(user_to_recieve=account)
    context     =   {
        'RECIEVED': orders, 
    }    
    return render(request, "dashboard/received_items.html",context)

def login(request):
    if request.method   == 'POST':
        email       = request.POST['email']
        password    = request.POST['password']
        
        user        = auth.authenticate(email=email, password=password)

        if user != None:
            auth.login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid login details')
            return redirect('login')
    return render(request, 'accounts/login.html')            

@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'You are logged out')
    return redirect('login')
    return render(request, 'accounts/logout.html')


def forgotpassword(request):
    if request.method  == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email=email)

            current_site    = get_current_site(request)
            subject    = 'Reset your password'
            message  = render_to_string('accounts/reset_password_email.html',{
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            }) 
            from_mail = settings.EMAIL_HOST_USER
            recipient_list = [email]
            send_mail(subject,message, from_mail,recipient_list, fail_silently=True)

            messages.success(request, "Password reset email has been sent")
            return redirect('login')
        else:
            messages.error(request, 'Sorry!. Account does not exist')        
            return redirect('forgot_password')

    return render(request, 'accounts/forgot_password.html')

def validate_password_reset(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account.objects.get(pk=uid)
    except:
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid 
        messages.success(request, 'Reset your password')
        return redirect('reset_password')   
    else:
        messages.error(request, 'Reset password link expired')    
        return redirect('forgot_password')

def reset_password(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if confirm_password != password:
            messages.error(request, "Passwords do not match")
            return redirect('reset_password')
        else:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password change successful')
            return redirect('login')    
    return render(request, 'accounts/reset_password.html')        

@login_required(login_url='login')
def my_blogs(request):
    blogs               = Blog.objects.filter(author__email=request.user.email) 

    blogs_p             = Paginator(blogs, 8)
    blogs_page_number   = request.GET.get('page')
    blogs_object        = blogs_p.get_page(blogs_page_number)

    context     = {
        'BLOG_OBJECT': blogs_object,
    }
    return render(request, 'dashboard/my_blogs.html',context)   

@login_required(login_url='login')
def view_items(request):
    user = request.user.email
    account = Account.objects.get(email=user)
    if account.is_staff != True:
        messages.error(request, "Only administrators are allowed to view this page")
        return redirect('home')
    
    orders = OrderItem.objects.filter(product__owner=account).order_by('-date_added')
    p               = Paginator(orders, 6) 
    page_number     = request.GET.get('page')
    page_obj        = p.get_page(page_number)
    context = {
        'PAGE_OBJ': page_obj,
        'USER': account,
    } 
    return render(request,'dashboard/items_pending.html', context)