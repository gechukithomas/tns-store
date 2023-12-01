from django.contrib import admin
from accounts.models import Account
from .models import  OrderItem, cancelled_order, delivered_items

class  OrderItemAdmin(admin.ModelAdmin):
    list_display                = ('product', 'request_user',)

    def has_add_permission(self, request,obj=OrderItem()):
        user = request.user.email
        account = Account.objects.get(email=user)
        if account.is_superadmin != True:
            return False 
        else:
            return True       
    def has_view_permission(self, request,obj=OrderItem()):
        user = request.user.email
        account = Account.objects.get(email=user)
        if account.is_superadmin != True:
            return False        
        else:
            return True
    def has_change_permission(self, request,obj=OrderItem()):
        user = request.user.email
        account = Account.objects.get(email=user)
        if account.is_superadmin != True:
            return False
        else:
            return True        
    def has_delete_permission(self, request,obj=OrderItem()):
        user = request.user.email
        account = Account.objects.get(email=user)
        if account.is_superadmin != True:
            return False 
        else:
            return True            
class CancelledOrderAdmin(admin.ModelAdmin):
    list_display =  ['user','product', 'date']

    def has_add_permission(self, request,obj=OrderItem()):
        user = request.user.email
        account = Account.objects.get(email=user)
        if account.is_superadmin != True:
            return False
        else:
            return True
    def has_view_permission(self, request,obj=OrderItem()):
        user = request.user.email
        account = Account.objects.get(email=user)
        if account.is_superadmin != True:
            return False    
        else:
            return True
    def has_change_permission(self, request,obj=OrderItem()):
        user = request.user.email
        account = Account.objects.get(email=user)
        if account.is_superadmin != True:
            return False  
        else:
            return True      
    def has_delete_permission(self, request,obj=OrderItem()):
        user = request.user.email
        account = Account.objects.get(email=user)
        if account.is_superadmin != True:
            return False 
        else:
            return True    
class DeliveredItemsAdmin(admin.ModelAdmin):
    list_display =  ['user_to_recieve','product_name', 'quantity']                
    def has_add_permission(self, request,obj=OrderItem()):
        user = request.user.email
        account = Account.objects.get(email=user)
        if account.is_superadmin != True:
            return False
        else:
            return True
    def has_view_permission(self, request,obj=OrderItem()):
        user = request.user.email
        account = Account.objects.get(email=user)
        if account.is_superadmin != True:
            return False    
        else:
            return True
    def has_change_permission(self, request,obj=OrderItem()):
        user = request.user.email
        account = Account.objects.get(email=user)
        if account.is_superadmin != True:
            return False 
        else:
            return True       
    def has_delete_permission(self, request,obj=OrderItem()):
        user = request.user.email
        account = Account.objects.get(email=user)
        if account.is_superadmin != True:
            return False 
        else:
            return True    
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(cancelled_order, CancelledOrderAdmin)

admin.site.register(delivered_items, DeliveredItemsAdmin)