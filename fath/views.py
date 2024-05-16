from typing import Any
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.http import HttpResponse
from . import models 
from .utils import CartAuthenTicatedUser
from shop import settings
from django.urls import reverse
import stripe

from django.core.mail import send_mail

# Create your views here.
from django.contrib.auth.models import User , AbstractBaseUser

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


def index(request):
    posts = models.Product.objects.all()
    for post in posts:
        rating = models.Rating.objects.all()
        post.user_rating = rating.rating if rating else 0
    return render(request, "fath/shop-detail.html")



class ShopDetail(DetailView):
    model = models.Product
    context_object_name = 'product'
    template_name = 'fath/shop-detail.html'
    extra_context = {
        'categories': models.Category.objects.filter(parent=None) 
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = models.Product.objects.get(slug=self.kwargs['slug'])
        rating = models.Rating.objects.filter(product=product, user=self.request.user).first()
        context['user_rating']= rating.rating if rating else 0
        return context

def rate(request, product_id, rating):
    product = models.Product.objects.get(pk=product_id)
    models.Rating.objects.filter(product=product, user=request.user).delete()
    product.rating_set.create(user=request.user, rating=rating)
    return redirect('shop_detail' , slug=product.slug)




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



# def shop_detail(request, product_id):
#     product = models.Product.objects.get(pk=product_id)
#     categories = models.Category.objects.filter(parent=None)
#     products = models.Product.objects.all()
#     context = {
#         'product':product,
#         'categories':categories,
#         'products':products
#     }
#     return render(request, 'fath/shop-detail.html', context)


def cart(request):
    cart_info = CartAuthenTicatedUser(request).get_cart_info()
    context = {
        'order_products':cart_info['order_products'],
        'cart_total_price':cart_info['cart_total_price'],
        'cart_total_quantity':cart_info['cart_total_quantity']
    }
    return render(request, 'fath/cart.html', context)


def chackout(request):
    return render(request, 'fath/chackout.html')


def testimonial(request):
    return render(request, 'fath/testimonial.html')


def error_page(request):
    return render(request, 'fath/404.html')


def contact(request):
    return render(request, 'fath/contact.html')



def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        password_confirm = request.POST['password-confirm']
        if password==password_confirm:
            User.objects.create_user(
                username=username,
                password=password
            )
    return render(request, 'fath/register.html')


def to_cart(request, product_id, action):
    if request.user.is_authenticated:
        CartAuthenTicatedUser(request, product_id, action)
        current_page = request.META.get('HTTP_REFERER', 'index')
        return redirect(current_page)
    return HttpResponse('Iltimos avval royhatdan o`ting')


def create_checkout_sessions(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    user_cart = CartAuthenTicatedUser(request)
    cart_info = user_cart.get_cart_info()
    total_price = cart_info['cart_total_price']
    total_quantity = cart_info['cart_total_quantity']
    session = stripe.checkout.Session.create(
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': 'Online Shop mahsulotlari'
                },
                'unit_amount': int(total_price * 100)
            },
            'quantity': total_quantity
        }],
        mode='payment',
        success_url=request.build_absolute_uri(reverse('success')),
        cancel_url=request.build_absolute_uri(reverse('success')),
    )
    return redirect(session.url, 303)



def success_payment(request):
    return render(request, 'fath/success.html')





def send_message_to_client(request):
    send_mail(
        "Bizda aktsiya",
        "Abduvohid 😝😝",
        settings.EMAIL_HOST_USER,
        ["azizxonn791@gmail.com"],
        fail_silently=False,
    )
    return redirect('success')