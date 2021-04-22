from django.db import models
from django.utils.text import slugify
from django.urls import reverse

from accounts.models import User
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('restaurants:restaurant_list_by_category',
                        args=[self.slug])
    


class Restaurant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name='restaurants', on_delete=models.CASCADE)
    name = models.CharField(db_index=True, max_length=200)
    slug = models.SlugField(db_index=True, max_length=200)
    phone_no = PhoneNumberField()
    website_link = models.URLField(max_length=200, blank=True)
    facebook_link = models.URLField(max_length=200, blank=True)
    logo = models.ImageField(upload_to='restaurants/logos', blank=True)
    description = models.TextField(blank=True)
    open_hour = models.TimeField(auto_now=False, auto_now_add=False)
    close_hour = models.TimeField(auto_now=False, auto_now_add=False)
    available = models.BooleanField(default=True)
    created = models.TimeField(auto_now_add=True)
    updated = models.TimeField(auto_now=True)

    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)
    
    def __str__(self):
        return f'{self.name} for user {self.user.username}'
        
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('restaurants:restaurant_detail',
                        args=[self.id,self.slug])
    
    