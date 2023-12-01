from django.db import models
from accounts.models import Account, UserProfile
from datetime import datetime
from django.urls import reverse
from accounts.models import Account
from django.db.models import Count
from django_resized import  ResizedImageField
from django.utils import timezone
# Create your models here.
class Blog(models.Model):
    BLOG_CATEGORY= (
        ('technology', 'TECHNOLOGY'),
        ('lifestyle', 'LIFESTYLE'),
        ('fashion', 'FASHION'),
        ('art', 'ART'),
        ('food', 'FOOD'),
        ('travel', 'TRAVEL'),
    )
    VARIATION_CHOICES = (
        ('blog', 'PersonalBlog'),
        ('service', 'Service')
    )
    author              = models.ForeignKey(Account, on_delete=models.DO_NOTHING ,editable=False)
    category            = models.CharField(max_length=20, choices=BLOG_CATEGORY, blank=True)
    variation           = models.CharField(max_length=15, choices=VARIATION_CHOICES, blank=True,  default="blog")
    title               = models.CharField(max_length=150, blank=True)
    date_added          = models.DateTimeField(default=timezone.now, blank=True)
    short_description   = models.CharField(max_length=30, blank=True)
    description         = models.TextField(max_length=250, blank=True, )
    status              = models.BooleanField(default=True, blank=True)
    image               = ResizedImageField(upload_to='blogs/images')
     

    def get_author_profile(self):
        user_profile     =  UserProfile.objects.get(user=self.author)
        return user_profile     

    def get_total_views(self):
        views   = BlogViews.objects.filter(blog=self).count()
        return views
    def get_total_comments(self):
        comments = BlogComment.objects.filter(blog=self).count()
        return comments 
    def get_blog_url(self):
        return reverse('single_blog', args=[self.category, self.title, self.id])



    def __str__(self):
        return self.title
class BlogViews(models.Model):
    viewed_user         = models.CharField(max_length=50, blank=True)
    blog                = models.ForeignKey(Blog, on_delete=models.CASCADE)
    views               = models.IntegerField()
    date_viewed         = models.DateTimeField(default=timezone.now, blank=True)

    class Meta:
        verbose_name_plural = "BlogViews"

    def __str__(self):
        return self.blog.title


class BlogComment(models.Model):
    comment_user        = models.ForeignKey(Account, on_delete=models.CASCADE)
    blog                = models.ForeignKey(Blog, on_delete=models.CASCADE)
    comment             = models.TextField(max_length=200, blank=True)
    date_added          = models.DateTimeField(default=timezone.now, blank=True)

    class Meta:
        verbose_name_plural = "BlogComment"
        
    def __str__(self):
        return self.comment

class BlogCommentReply(models.Model):
    comment_reply_user  = models.ForeignKey(Account, on_delete=models.CASCADE)
    blog                = models.ForeignKey(BlogComment, on_delete=models.CASCADE)
    reply               = models.TextField(max_length=150, blank=True)
    date_added          = models.DateTimeField(default=timezone.now ,blank=True)

    class Meta:
        verbose_name_plural = "BlogCommentReply"
    def __str__(self):
        return self.reply

