from django.db import models
from django.contrib.auth.models import User
from shop.models import Product
from accounts.models import Account
from django.urls import reverse
from django.utils import timezone 
# Create your models here.
   
class OrderItem(models.Model):
    product                 = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity                = models.IntegerField()
    is_active               = models.BooleanField(default=True)
    date_added              = models.DateTimeField(default=timezone.now, blank=True)
    request_user            = models.ForeignKey(Account, on_delete=models.CASCADE)
    def purge_order(self):
        return reverse('purge_order', args=[self.product.id])

    def sub_total(self):
        return self.product.price * self.quantity
    class Meta:
        verbose_name_plural = 'orderitem'

    def __str__(self):    
        string_product = str(self.product)
        return string_product


class cancelled_order(models.Model):
    user                    = models.CharField(max_length=30,blank=True)
    product                 = models.CharField(max_length=30, blank=True)
    product_id              = models.CharField(max_length=10, blank=True)
    date                    = models.DateTimeField(default=timezone.now, blank=True)

    class Meta:
        verbose_name_plural = "CancelledOrders"

    def __str__(self):
        return self.product

class recieved_orders(models.Model):
    user                    = models.CharField(max_length=30, blank=True) 
    product                 = models.CharField(max_length=30, blank=True)
    date                    = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product
        

class delivered_items(models.Model):
    user_to_recieve         = models.ForeignKey(Account, on_delete=models.CASCADE, blank=True)
    trader                  = models.CharField(max_length=20, blank=True)
    product_name            = models.CharField(max_length=30, blank=True)       
    quantity                = models.IntegerField(blank=True)
    price                   = models.IntegerField()
    image                   = models.ImageField(upload_to='delivered_items', blank=True)
    received_date           = models.DateTimeField(default=timezone.now, blank=True)
    
    class Meta:
        verbose_name_plural = "DeliveredItems"

    def __str__(self):
        return self.product_name

        