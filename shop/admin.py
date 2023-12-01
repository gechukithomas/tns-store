from django.contrib import admin
from .models import Category, Subcategory, Variation, Product, Review, PopularProduct
from django.utils.html import format_html
from accounts.models import Account
from django.core.exceptions import PermissionDenied
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields                 = {'slug': ( 'category_name',)}
    list_display                        = ['category_name'] 

    def has_change_permission(self, request, obj=Category):
        account = Account.objects.get(email=request.user.email)
        if account.is_superadmin:
            return True
        else: 
            return False 
    def has_delete_permission(self, request, obj=Category):
        account = Account.objects.get(email=request.user.email)
        if account.is_superadmin:
            return True
        else: 
            return False         
    
    def has_add_permission(self, request, obj=Category):
        account = Account.objects.get(email=request.user.email)
        if account.is_superadmin:
            return True
        else: 
            return False        
class SubcategoryAdmin(admin.ModelAdmin):
    prepopulated_fields                 = {'slug': ('subcategory_name',)}
    list_display                        = ['category', 'subcategory_name' ]    
   
    def has_add_permission(self, request, obj=Subcategory):
        account = Account.objects.get(email=request.user.email)
        if account.is_superadmin:
            return True
        else: 
            return False
    def has_change_permission(self, request, obj=Subcategory):
        account = Account.objects.get(email=request.user.email)
        if account.is_superadmin:
            return True
        else: 
            return False     
    def has_delete_permission(self, request, obj=Subcategory):
        account = Account.objects.get(email=request.user.email)
        if account.is_superadmin:
            return True
        else: 
            return False     
class VariationAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('variation',)}
    list_display = ['category', 'subcategory', 'variation']

class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields                 = {'slug': ('product_name',)}    

    list_display                        = ['owner', 'id', 'product_name', 'category', 'subcategory', 'color', 'price', 'is_available', 'stock']
    search_fields = ['product_name', 'color']
    #exclude = ['owner']
    def has_delete_permission(self, request, obj=Product):
        account = Account.objects.get(email=request.user.email)
        if account.is_superadmin:
            return True
        else: 
            return False

    def save_model(self, request, obj, form, change):
        account = Account.objects.get(email=request.user.email)
        obj.owner = account
        super().save_model(request, obj, form, change)        

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        user = request.user.email
        account = Account.objects.get(email=user)
        return qs if account.is_superadmin else qs.filter(owner__email=user)       
class ReviewAdmin(admin.ModelAdmin):               
    list_display    = ['review', 'user', 'rating','product', 'owner', 'admin_get_id','created_date']
    
    def has_view_permission(self, request, obj=Review):
        account = Account.objects.get(email=request.user.email)
        if account.is_superadmin:
            return True
        else: 
            return False
    def has_add_permission(self, request, obj=Review):
        account = Account.objects.get(email=request.user.email)
        if account.is_superadmin:
            return True
        else: 
            return False     
    def has_change_permission(self, request, obj=Review):
        account = Account.objects.get(email=request.user.email)
        if account.is_superadmin:
            return True
        else: 
            return False        
    def has_delete_permission(self, request, obj=Review):
        account = Account.objects.get(email=request.user.email)
        if account.is_superadmin:
            return True
        else: 
            return False

  

class PopularProductAdmin(admin.ModelAdmin):
    list_display  = ['product', 'hits'] 

    def has_view_permission(self, request, obj=PopularProduct):
        account = Account.objects.get(email=request.user.email)
        if account.is_superadmin:
            return True
        else: 
            return False
    def has_add_permission(self, request, obj=PopularProduct):
        account = Account.objects.get(email=request.user.email)
        if account.is_superadmin:
            return True
        else: 
            return False     
    def has_change_permission(self, request, obj=PopularProduct):
        account = Account.objects.get(email=request.user.email)
        if account.is_superadmin:
            return True
        else: 
            return False        
    def has_delete_permission(self, request, obj=PopularProduct):
        account = Account.objects.get(email=request.user.email)
        if account.is_superadmin:
            return True
        else: 
            return False

    
admin.site.register(Category, CategoryAdmin)
admin.site.register(Subcategory, SubcategoryAdmin)
admin.site.register(Variation, VariationAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(PopularProduct, PopularProductAdmin)
