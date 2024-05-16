from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexList.as_view() , name='index'),
    path('shop/', views.ShopList.as_view() , name='shop'),
    path('sorting/<slug:key_name>', views.SortingProductList.as_view(), name='sorting'),
    path('subcategory/<slug:slug>', views.SortingBySubcategories.as_view(), name='subcategory'),
    path('shop-detail/<slug:slug>', views.ShopDetail.as_view(), name='shop_detail'),
    path('rate/<int:product_id>/<int:rating>/', views.rate),
    path('register/', views.register, name='register'),
    path('payment/', views.create_checkout_sessions, name='payment'),
    path('succsess/', views.success_payment, name='success'),

    path('cart/', views.cart, name='cart'),
    path('to_cart/<int:product_id>/<str:action>/', views.to_cart, name='to_cart'),
    path('chackout/', views.chackout, name='chackout'),
    path('testimonial/', views.testimonial, name='testimonial'),
    path('404/', views.error_page, name='404'),
    path('contact/', views.contact, name='contact'),
]
 