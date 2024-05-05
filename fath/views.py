from typing import Any
from django.shortcuts import render
from django.views.generic import ListView
from . import models 
# Create your views here.


class IndexList(ListView):
    model = models.Product
    template_name = 'fath/index.html'
    context_object_name = 'products'
    extra_context = {
        'categories': models.Category.objects.filter(parent=None),
        'products': models.Product.objects.all().order_by('-id')
    }


class ShopList(IndexList):
    template_name = 'fath/shop.html'
  


class SortingProductList(ShopList):
    def get_context_data(self, object_list=None , **kwargs) :
        context = super().get_context_data(**kwargs)
        products = models.Product.objects.filter(filter_choice=self.kwargs['key_name'])
        context['products'] = products
        return context
        


class SortingBySubcategories(ShopList):
    def get_context_data(self, object_list=None , **kwargs) :
        context = super().get_context_data(**kwargs)
        subcategory = models.Category.objects.get(slug=self.kwargs['slug'])
        context['products'] = subcategory.product_set.all()
        return context

# def sorting(request, key_name):
#     context = {
#         'products': models.Product.objects.filter(filter_choice=key_name),
#         'categories': models.Category.objects.filter(parent=None)
#     }

#     return render(request, 'fath/shop.html', context)


# def sorting_by_subcategory(request, slug):
#     subcategory = models.Category.objects.get(slug=slug)
#     context = {
#         'categories':models.Category.objects.filter(parent=None),
#         'products': subcategory.product_set.all()
#     }
#     return render(request, 'fath/shop.html', context)

# def index(request):
#     categories = models.Category.objects.all()
#     products = models.Product.objects.all().order_by('-id')
#     cantex = {
#         'categories':categories,
#         'products':products,
#     }
    
#     return render(request, 'fath/index.html', cantex)


# def shop(request):
#     return render(request, 'fath/shop.html')


def shop_detail(request, product_id):
    product = models.Product.objects.get(pk=product_id)
    categories = models.Category.objects.filter(parent=None)
    products = models.Product.objects.all()
    context = {
        'product':product,
        'categories':categories,
        'products':products
    }
    return render(request, 'fath/shop-detail.html', context)


def cart(request):
    return render(request, 'fath/cart.html')


def chackout(request):
    return render(request, 'fath/chackout.html')


def testimonial(request):
    return render(request, 'fath/testimonial.html')


def error_page(request):
    return render(request, 'fath/404.html')


def contact(request):
    return render(request, 'fath/contact.html')

