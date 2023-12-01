from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account , UserProfile, contact_page_messages
from django.utils.html import format_html
from django.contrib.auth.models import User
from shop.models import Product
from django.http import HttpResponse
# Register your models here.
class AccountAdmin(UserAdmin):
    list_display                = ('email','id' ,'is_staff', 'first_name', 'last_name', 'username', 'last_login', 'is_active',)
    list_display_links          = ('email', 'first_name', 'last_name')
    readonly_fields             = ('last_login', 'date_joined')
    ordering                    = ('-date_joined',)
    filter_horizontal           = ()       
    list_filter                 = ()
    fieldsets                   = ()
    def has_add_permission(self, request, obj=Account):
        account = Account.objects.get(email=request.user.email)
        if account.is_superadmin:
            return True
        else:  
            return False
    def has_view_permission(self, request, obj=Account):
        account = Account.objects.get(email=request.user.email)
        if account.is_superadmin:
            return True
        else:     
            return False
    def has_change_permission(self, request, obj=Account):
        account = Account.objects.get(email=request.user.email)         
        if account.is_superadmin: 
            return True
        else:
            return False
    def has_delete_permission(self, request, obj=Account):
        account = Account.objects.get(email=request.user.email)         
        if account.is_superadmin:
            return True
        else:
            return False
class UserProfileAdmin(admin.ModelAdmin):
    
    def image_show(self, object):
            return format_html('<img src="{}" width="50" style="border-radius:50%; "> '.format(object.image.url))
    image_show.short_description = 'Image'
    list_display        = ['image_show','user']
    def has_add_permission(self, request, obj=Account):
        account = Account.objects.get(email=request.user.email)
        if account.is_superadmin:
            return True
        else:  
            return False
    def has_delete_permission(self, request, obj=Account):
        account = Account.objects.get(email=request.user.email)
        if account.is_superadmin:
            return True
        else:  
            return False        
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        user = request.user.email
        account = Account.objects.get(email=user)
        return qs if account.is_superadmin else qs.filter(user__email=user)

class contact_page_messagesAdmin(admin.ModelAdmin):
    list_display      = ['username', 'email', 'subject', 'message']

    def has_add_permission(self, request, obj=Account):
        account = Account.objects.get(email=request.user.email)
        if account.is_superadmin:
            return True
        else:  
            return False
    def has_view_permission(self, request, obj=Account):
        account = Account.objects.get(email=request.user.email)
        if account.is_superadmin:
            return True
        else:     
            return False
    def has_change_permission(self, request, obj=Account):
        account = Account.objects.get(email=request.user.email)         
        if account.is_superadmin: 
            return True
        else:
            return False
    def has_delete_permission(self, request, obj=Account):
        account = Account.objects.get(email=request.user.email)         
        if account.is_superadmin:
            return True
        else:
            return False

admin.site.register(Account, AccountAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(contact_page_messages, contact_page_messagesAdmin)