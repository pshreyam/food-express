from decimal import Decimal
from django.conf import settings

from .models import Cart as cart_model, CartItem
from coupons.models import Coupon

class Cart(object):

    def __init__(self,request):
        try:
            if request.user.is_customer:
                self.customer = request.user.customer
            try:
                cart = self.customer.cart
            except Exception:
                cart = cart_model.objects.create(customer=self.customer)
            self.cart = cart
        except Exception:
            self.cart = None
        
        #store the current applied coupon
        #self.coupon_id = self.session.get('coupon_id')

    
    def add(self, food, quantity=1, override_quantity=False):
        try:
            cart_item = CartItem.objects.get(cart=self.cart, food=food)
        except:
            cart_item = CartItem.objects.create(cart=self.cart, food=food,
                                    quantity=0, price=food.get_selling_price)
        
        if override_quantity:
            cart_item.quantity = quantity
        else:
            cart_item.quantity += quantity
        cart_item.save()
    
    def remove(self, food):
        cart_item = CartItem.objects.get(cart=self.cart, food=food)
        if cart_item:
            cart_item.delete()
    
    def __len__(self):
        cart_items = self.get_all_items()
        return sum(item.quantity for item in cart_items)

    def get_total_price(self):
        cart_items = self.get_all_items()
        return sum(Decimal(item.price) * item.quantity for item in cart_items)
    
    def get_all_items(self):
        return CartItem.objects.filter(cart=self.cart)

    def clear(self):
        self.cart.delete()
    
    def add_coupon(self, coupon_code):
        self.cart.coupon_code = coupon_code
        self.cart.save()

    @property
    def coupon(self):
        if self.cart.coupon_code:
            try:
                return Coupon.objects.get(code__iexact = self.cart.coupon_code)
            except Coupon.DoesNotExist:
                pass
        return None
    
    def identity(self):
        return self.cart.id

    def get_discount(self):
        if self.cart.coupon_code:
            return (self.coupon.discount / Decimal(100)) * self.get_total_price()
        return Decimal(0)
    
    def get_total_price_after_discount(self):
        return self.get_total_price() - self.get_discount()
    
    def get_total_price_in_paisa(self):
        return self.get_total_price_after_discount() * 100
            