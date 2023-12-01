from django.db import models
from django.urls import reverse
from accounts.models import Account
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django_resized import ResizedImageField
class Category(models.Model):
    category_name           = models.CharField(max_length=50, blank=True)
    slug                    = models.SlugField(max_length=50, blank=True)

    class Meta:
        verbose_name_plural = "category"

    def __str__(self):
        return self.category_name

class Subcategory(models.Model):
    category                = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory_name        = models.CharField(max_length=50, blank=True)
    slug                    = models.SlugField(max_length=50, blank=True)

    class Meta:
        verbose_name_plural = "subcategory"

    def __str__(self):
        return self.subcategory_name

class Variation(models.Model):
    category                = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory             = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    variation               = models.CharField(max_length=20, blank=True)
    slug                    = models.SlugField(max_length=20, blank=True)

    class Meta:
        verbose_name_plural = "variation"

    def variation_list(request, SUBCATEGORY):
        variation_list      = Variation.objects.filter(subcategory__slug=SUBCATEGORY)
        return variation_list

    def __str__(self):
        return self.variation

class Product(models.Model):
    
    class GenderChoice(models.TextChoices):
        MEN     = 'men',    _('Men')
        WOMEN   = 'women',   _('Women')
        BOTH    = 'both',     _('Both')
    class AgeChoice(models.TextChoices):
        CHILD   = 'child', _('Child')
        ADULT   = 'adult',   _('Adult')
    class ColorChoice(models.TextChoices):
        BLUE    = 'blue',  _('Blue')
        RED     = 'red',    _('Red')
        WHITE   = 'white',    _('White')
        GREY    = 'grey',      _('Grey')  
        ORANGE  = 'orange',      _('Orange')
        GREEN   = 'green',        _('Green')
        PURPLE  = 'purple',        _('Purple')
        PINK    = 'pink',           _('Pink')
        BLACK   = 'black',           _('Black')
        BROWN   = 'brown',            _('Brown')
        YELLOW  = 'yellow',            _('Yellow')

    owner                   = models.ForeignKey(Account, on_delete=models.CASCADE, editable=False)
    category                = models.ForeignKey(Category, on_delete=models.CASCADE) 
    subcategory             = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    variation               = models.ForeignKey(Variation, on_delete=models.CASCADE)
    age                     = models.CharField(max_length=10, choices=AgeChoice.choices, default=AgeChoice.ADULT,)
    gender                  = models.CharField(max_length=10, choices=GenderChoice.choices,default=GenderChoice.MEN,)
    color                   = models.CharField(max_length=15, choices=ColorChoice.choices, default=ColorChoice.BLACK,)
    product_name            = models.CharField(max_length=50)
    slug                    = models.SlugField(max_length=50)
    description             = models.TextField(max_length=250)
    region                  = models.TextField(max_length=100)
    price                   = models.IntegerField()
    stock                   = models.IntegerField()
    date_added              = models.DateTimeField(default=timezone.now, blank=True) 
    is_available            = models.BooleanField(default=True)
    image1                  = ResizedImageField(upload_to='product/image1')
    image2                  = ResizedImageField(upload_to='product/image2')
    image3                  = ResizedImageField(upload_to='product/image3')


    class Meta:
        verbose_name_plural = "product"
 
    def get_url(self):
        return reverse('single_product', args=[self.category.slug, self.subcategory.slug, self.variation.slug, self.slug, self.id ])
    
    def averageReview(self):
        reviews = Review.objects.filter(product=self).count()   
        return reviews
    
    def __str__(self):
        return self.product_name   

class PopularProduct(models.Model):
    product         = models.ForeignKey(Product, on_delete=models.CASCADE)
    hits            = models.IntegerField()
    def __str__(self):
        return self.product.product_name

class Review(models.Model):
    product         = models.ForeignKey(Product, on_delete=models.CASCADE)
    user            = models.ForeignKey(Account, on_delete=models.CASCADE)
    review          = models.TextField(max_length=500)
    rating          = models.IntegerField(default=0)
    created_date    = models.DateTimeField(default=timezone.now, blank=True)
    status          = models.BooleanField(default=True)

    class META:
        verbose_name_plural = "Review"
    def admin_get_id(self):
        return self.product.pk 
    def owner(self):
        return self.product.owner.username
    def __str__(self):
        return str(self.product)

        