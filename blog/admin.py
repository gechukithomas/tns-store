from django.contrib import admin
from django.http import HttpResponse
from accounts.models import Account
from .models import Blog, BlogViews, BlogComment, BlogCommentReply
# Register your models here.
class BlogAdmin(admin.ModelAdmin):
    list_display            = ['category', 'variation', 'author','title']
    
    def has_delete_permission(self, request, obj=Blog):
        account = Account.objects.get(email=request.user.email)
        if account.is_superadmin:
            return True
        else: 
            return False

    def save_model(self, request, obj, form, change):
        account = Account.objects.get(email=request.user.email)
        obj.author = account
        super().save_model(request, obj, form, change)        

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        user = request.user.email
        account = Account.objects.get(email=user)
        return qs if account.is_superadmin else qs.filter(author__email=user) 

class BlogViewsAdmin(admin.ModelAdmin):
    list_display            = ['viewed_user', 'blog', 'views', 'date_viewed']    

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

class BlogCommentAdmin(admin.ModelAdmin):
    list_display            = ['comment_user', 'comment','blog']     


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
class BlogCommentReplyAdmin(admin.ModelAdmin):
    list_display            = ['comment_reply_user', 'reply','blog']  

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
            
              
admin.site.register(Blog, BlogAdmin)
admin.site.register(BlogViews, BlogViewsAdmin)
admin.site.register(BlogComment, BlogCommentAdmin)
admin.site.register(BlogCommentReply, BlogCommentReplyAdmin)
