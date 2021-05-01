from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from phonenumber_field.modelfields import PhoneNumberField

from accounts.models import User
from foods.models import Food


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(db_index=True, max_length=200)
    profile_pic = models.ImageField(upload_to='customers/profile_pic', blank=True)
    phone_no = PhoneNumberField(region='NP')
    created = models.TimeField(auto_now_add=True)
    updated = models.TimeField(auto_now=True)

    class Meta:
        ordering = ('full_name',)
        index_together = (('id', 'user'),)
    
    def __str__(self):
        return f'Customer: {self.full_name} for user {self.user.username}'

class Order(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.SET_NULL,blank=True,null=True)
    complete=models.BooleanField(default=False,null=True,blank=True)
    date_ordered=models.DateTimeField(auto_now_add=True)
    transcation_id=models.CharField(max_length=200,null=True)

    
    def __str__(self):
        return str(self.id)



class OrderItem(models.Model):
    food=models.ForeignKey(Food,on_delete=models.SET_NULL,blank=True,null=True)
    order=models.ForeignKey(Order,on_delete=models.SET_NULL,blank=True,null=True)
    date_added=models.DateTimeField(auto_now_add=True)
    quantity=models.IntegerField(default=0,blank=True)

class ShippingAddress(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.SET_NULL,blank=True,null=True)
    order=models.ForeignKey(Order,on_delete=models.SET_NULL,blank=True,null=True)
    address=models.CharField(max_length=200,null=True)
    city=models.CharField(max_length=200,null=True)
    state=models.CharField(max_length=200,null=True)
    zipcode=models.CharField(max_length=200,null=True)
    date_added=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address