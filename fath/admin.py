# from django.apps import apps
from django.contrib import admin
from . import models
from django.utils.safestring import mark_safe
# Register your models here.


# all_models = apps.get_models()

# models_list = []

# for model in all_models:
#     if not admin.site.is_registered(model):
#         models_list.append(model)

# for model_class in models_list:
#     admin.site.register(model_class)

@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id','name','slug' ,'get_image')
    prepopulated_fields = {'slug': ('name',)}

    def get_image(self, category):
        if category.img:
         return mark_safe(f'<img src="{category.img.url}" width="75px;">')
        

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name','slug', 'body','price', 'dicount','quantity','category','created','get_image')
    list_display_links = ('id', 'name')

    def get_image(self, product):
        if product.img:
            return mark_safe(f'<img src="{product.img.url}" width="75px;">')
        
    prepopulated_fields = {'slug': ('name',)}
