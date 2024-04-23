from django.shortcuts import render

# Create your views here.


def index(request):
    return render(request, 'fath/index.html')


def shop(request):
    return render(request, 'fath/shop.html')


def shop_detail(request):
    return render(request, 'fath/shop-detail.html')


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

