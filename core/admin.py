from django.contrib import admin
from .models import Product,Shop,Sold,Cart
# Register your models here.
admin.site.register(Shop)
admin.site.register(Product)
admin.site.register(Sold)
admin.site.register(Cart)