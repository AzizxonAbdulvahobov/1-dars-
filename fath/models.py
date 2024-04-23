from django.db import models

# Create your models here.

"""Xali tugallanmagan modellar"""


class category(models.Model):
    name = models.TextField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class product(models.Model):
    category = models.ForeignKey(category, on_delete=models.CASCADE)
    img = models.ImageField(upload_to='product_img')
    name = models.CharField(max_length=255)
    body = models.TextField()
    price = models.IntegerField()