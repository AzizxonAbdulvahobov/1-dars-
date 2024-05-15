from . import models

class CartAuthenTicatedUser:
    def __init__(self, request, product_id=None, action=None):
        self.request = request


        if product_id and action:
             self.add_or_delete(product_id, action)


    def get_cart_info(self):
        customer, created = models.Customer.objects.get_or_create(
            user = self.request.user,

        )

        order, created, = models.Order.objects.get_or_create(
            customer=customer
        )

        order_products = order.orderproduct_set.all()
        return{
            'order':order,
            'order_products':order_products
        }

    def add_or_delete(self, product_id, action):
        order = self.get_cart_info()['order']
        product = models.Product.objects.get(pk=product_id)
        order_product , created = models.OrderProduct.objects.get_or_create(
            order=order,
            product=product
        )

        if action == 'add':
            order_product.quantity += 1
            product.quantity -= 1
        else:
            order_product.quantity -= 1
            product.quantity += 1

        order_product.save()
        product.save()

        if order_product.quantity <= 0:
            order_product.delete()