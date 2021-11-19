from django.db import models

# Create your models here.
class Shop(models.Model):
    name =  models.CharField(max_length=550,null=True,blank=True)
class BaseEntity(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

class Product(BaseEntity):
    shop = models.ForeignKey(Shop,on_delete=models.CASCADE)
    name = models.CharField(max_length=120)
    full_description = models.TextField(null=True,blank=True)
    current_stock = models.IntegerField(default=0)
    price = models.IntegerField(default=0)
    promotional_price = models.IntegerField(default=0)
    tag = models.CharField(max_length=10,null=True,blank=True)
    picture = models.ImageField(upload_to='product/%Y/%m/%d', default="avatar.png", blank=True)

    def __str__(self):
        return self.name

class Sold(BaseEntity):
    prod = models.ManyToManyField(Product)
    customer_fname = models.CharField(max_length=550,null=True,blank=True)
    customer_email = models.CharField(max_length=550,null=True,blank=True)
    customer_address = models.CharField(max_length=550,null=True,blank=True)
    customer_lname = models.CharField(max_length=550,null=True,blank=True)
    customer_phone = models.CharField(max_length=550,null=True,blank=True)
    payment_method = models.CharField(max_length=550,null=True,blank=True)
    total_amount = models.CharField(max_length=550,null=True,blank=True)
    completed = models.BooleanField(default=False)
    
class Cart(BaseEntity):
    products = models.ManyToManyField(Product, null=True)
    total = models.DecimalField(max_digits=100, decimal_places=2, default=0.00)
    active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.total)