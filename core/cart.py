from decimal import Decimal
from django.conf import settings
from django.forms.models import model_to_dict
from .models import Product

class Cart(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1, price=None, update_quantity=False):
        product_id = str(product.id)
        print(price)
        if price == None:
            price = product.price
        if product_id not in self.cart:
            self.cart[product_id] = {'id': product.pk,'image': product.picture.url,'quantity': 0, 'price': str(price)}
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
            self.cart[product_id]['price'] = price
        else:
            self.cart[product_id]['quantity'] += quantity
            self.cart[product_id]['price'] = price
        self.save()

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            self.cart[str(product.id)]['product'] = product

        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def get_total_products(self):
        i=0
        for item in self.cart.values():
            i=i+1
        return  i

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True
