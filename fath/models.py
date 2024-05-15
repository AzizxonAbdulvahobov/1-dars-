from django.db import models
from django.contrib.auth.models import User
# Create your models here.

"""Xali tugallanmagan modellar"""


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    img = models.ImageField(upload_to='category_img/')
    slug = models.SlugField(blank=True, null=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE,blank=True,null=True,related_name='subcategories')

    def __str__(self):
        return self.name
    
FILTER_CHOICES = {
    'po':'Popularity',
    'org':'Organic',
    'fan':'Fantastic'
}
    


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    filter_choice = models.CharField(max_length=255, choices=FILTER_CHOICES, null=True)
    img = models.ImageField(upload_to='product_img/')
    name = models.CharField(max_length=255)
    body = models.TextField()
    price = models.FloatField()
    dicount = models.FloatField(blank=True, null=True)
    quantity = models.FloatField()
    slug = models.SlugField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name
    
    @property
    def discount(self):
        if self.dicount:
            return self.price - self.dicount
        


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def __str__(self) :
        return f"{self.product.name}:{self.rating}"
    





class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    first_name = models.CharField(max_length=255, null=True, default='')
    last_name = models.CharField(max_length=255, null=True, default='')


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    created = models.DateTimeField(auto_now_add=True)
    is_activ = models.BooleanField(default=True)
    @property
    def get_cart_total_price(self):
        order_products = self.orderproduct_set.all()
        total_price = sum([product.get_cart_price for product in order_products])
        return total_price
    
    @property
    def get_cart_total_quantity(self):
        order_products = self.orderproduct_set.all()
        total_quantity =sum([product.quantity for product in order_products])
        return total_quantity
    

class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0)
    added = models.DateTimeField(auto_now_add=True)
    @property
    def get_cart_price(self):
        total_price = self.quantity * self.product.price
        return total_price


class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    addres = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    distict = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)


 