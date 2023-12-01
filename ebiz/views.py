from django.shortcuts import render, redirect
from accounts.forms import Contact_page_messages
from shop.models import Product
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages

def home(request):
    total_count     = Product.objects.all().count()
    items           = Product.objects.all().filter(is_available=True).order_by("?")[0:8]
    
    context         = {
        'ITEMS':     items,
    }
    return render(request, 'index.html', context)

def contact(request):
    if request.method == 'POST':
        username        =   request.POST['username']
        email_address   =   request.POST['email']
        subject         =   request.POST['subject']
        message         =   request.POST['message']
  
        message1         = "Hello Thomas\n {} has the following message\n\n {}".format(username, message)
        print(message1)
        from_email      =  email_address
        recipient_list  = ['optimarsalmefranchis@gmail.com']
        send_mail(subject, message1, from_email, recipient_list, fail_silently=True)
        messages.success(request, "Your message has been successfully sent")
        return redirect('contact')
    return render(request, 'contact.html')