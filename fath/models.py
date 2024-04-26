from django.db import models

# Create your models here.

"""Xali tugallanmagan modellar"""


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    img = models.ImageField(upload_to='category_img/')
    slug = models.SlugField(blank=True, null=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
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
    
    


