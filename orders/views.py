from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from shop.models import Product, PopularProduct
from .models import  OrderItem, cancelled_order
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.contrib import messages
from accounts.models import Account
from django.template.loader import render_to_string
# Create your views here.
@login_required( login_url='login')
def orders(request, total=0, quantity=0, order_items=None):
    if request.user.is_staff :
        messages.error(request, "Sorry. You are not Authorised to view this page")
        return redirect('shop')
    user    =  request.user
    user    = str(user)
    account = Account.objects.get(email=user)
    try:
        order_items     = OrderItem.objects.filter(request_user=account, is_active=True)
        for order_item in order_items:
            total += (order_item.product.price * order_item.quantity)
            quantity += order_item.quantity
       
    except:
        pass
    context     = {
        'TOTAL':    total,
        'QUANTITY':     quantity,
        'ORDER_ITEMS':      order_items,
    }

    return render(request, 'orders.html', context)

  
def add_order(request,product_id):
    if request.user.is_authenticated == False:
        messages.error(request, "Please login to make order")
        return redirect("login")
    user    = request.user  
    user    = str(user)
    account = Account.objects.get(email=user)
    if account.is_staff == True:
        messages.error(request, "Sorry! Clients are not authorised to make orders")
        return redirect("shop")

    product    = Product.objects.get(id=product_id)   

    try:
        order_item      = OrderItem.objects.get(product=product, request_user=account)
        if order_item.quantity > 0:

            order_item.quantity     += 1
            order_item.save()
    except OrderItem.DoesNotExist:
        order_item  =   OrderItem.objects.create(
            product= product,
            quantity= 1,
            request_user= request.user,
        )
        order_item.save()
    try:     
        popular_product = PopularProduct.objects.get(product=product)
        popular_product.hits += 1
        popular_product.save()
    except:
        popular_product = PopularProduct.objects.create(
            product=    product,
            hits =+ 1,
        )        
    return redirect('orders')   
    context     = { 'ITEM':     item } 
    #return render(request, 'place_orders.html', context)
#Request user: remove order_item function
@login_required(login_url='login')
def remove_order(request, product_id):
    account     = Account.objects.get(email=request.user.email)
    product     = Product.objects.get(id=product_id)
    order_item  = OrderItem.objects.get(product=product, request_user=account)
    if order_item.quantity > 1:
        order_item.quantity -= 1
        order_item.save()
    else:
        order_item.delete()
    return  redirect('orders')        

@login_required(login_url='login')
def cancel_order(request, product_id):
    product = Product.objects.get(id=product_id)
    account = Account.objects.get(email=request.user.email)
    try:
        order_item =  OrderItem.objects.get(request_user=account, product=product)
    except: 
        messages.error(request, "An error occurred")
        return redirect('dashboard')
    item_to_delete = order_item.product.product_name    
    data = cancelled_order()
    data.user = account.email
    data.product = order_item.product.product_name
    data.product_id = order_item.product.id
    data.save()
    order_item.delete()
    context = {
        'product_name': item_to_delete,
        'my_mail': 'Optimarsalmefranchise@gmail.com',
        'my_number': '0704436540',
        'link': 'https://api.whatsapp.com/send?phone=+254704436540',
    }
    return render(request, 'dashboard/error.html', context)
