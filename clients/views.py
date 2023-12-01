from django.shortcuts import render, redirect
from orders.models import OrderItem, delivered_items
from django.utils import timezone
from accounts.models import Account
from django.conf import settings
from django.core.mail import send_mail
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from shop.models import Product
from .forms import AddProductForm
from shop.models import Category, Subcategory

# Create your views here.

@login_required(login_url='login')    
def delete_order(request, product_id):
    account         = Account.objects.get(email=request.user.email)
    try:
        product       = OrderItem.objects.get(product__id=product_id)
    except: 
        messages.error(request, "an error occurred. user may have deleted the order")
        return redirect('client_view_items')
    counter     = product.quantity
    product.delete()
    data = Product.objects.get(id=product_id)
    data.stock - counter
    data.save()
    messages.success(request, "Order removed successfully")

    new_data    = delivered_items()
    new_data.user_to_recieve = product.request_user
    new_data.trader     = data.owner.first_name
    new_data.product_name = data.product_name
    new_data.quantity   = product.quantity
    new_data.price      = data.tot
    new_data.save()

    return redirect('client_view_items')

