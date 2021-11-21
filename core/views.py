from django.shortcuts import render, get_object_or_404,redirect
from django.views.generic.base import TemplateView
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from .models import Product,Sold
from .cart import Cart
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.views import View
# Create your views here.
class Home(ListView):
    template_name = 'index.html'
    model = Product
    context_object_name = 'product'
    paginate_by = 20

    def get_queryset(self,*args,**kwargs):
        name = self.request.GET.get('search')
        object_list = self.model.objects.all()
        print(object_list)
        if name:
            object_list = object_list.filter(name__icontains=name)
        return object_list

class Contact(TemplateView):
    template_name = 'contact.html'
    

class Checkout(View):
    def get(self,request):
        cart = Cart(request)   
        context = {
            'cart': cart,
            'delivery':200,
        }
        template_name = 'checkout.html'
        return render(request, template_name,context)
    
    def post(self,request):
        fname = request.POST['fname']
        lname = request.POST['lname']
        address = request.POST['address']
        phone = request.POST['phone']
        email = request.POST['email']
        method = request.POST['method']
        
        
        instance = Sold()
        instance.customer_fname = fname
        instance.customer_lname = lname
        instance.customer_address = address
        instance.customer_phone = phone 
        instance.customer_email = email
        instance.payment_method = method
        instance.save()
        cart = Cart(request)   
        for item in cart:
            instance2 = Product.objects.get(id = item['id'])
            instance.prod.add(instance2)
        instance.save()
        cart.clear()
        messages.success(request, 'All your items has been ordered and we will contact you soon. Thank you ')
        return redirect('home')
        
class CartTemplate(View):
    def get(self, request):
        cart = Cart(request)   
        for item in cart:
            item['update_quantity_form'] = {'quantity': item['quantity'],'price': item['price']  ,'update': True,'image': item['image'],'id': item['id']}
        context = {
            'cart': cart,
            'delivery':200,
        }
        template_name = 'cart.html'
        return render(request, template_name,context)


# Add to cart views
def cart_add(request, id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=id)
    cart.add(product=product, quantity=1, update_quantity=False)
    messages.success(request, f'{product.name} has been added to cart.')
    return redirect('home')


# Remove Shopping Cart views
def cart_remove(request, id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=id)
    cart.remove(product)
    return redirect('cart')


# update Shopping Cart views
@require_POST
def cart_updated(request, id):
    number = None
    cart = Cart(request)
    if request.method == 'POST':
        if request.POST['submit'] == 'add':
            number = int(request.POST['number']) + 1
        else:
            number = int(request.POST['number']) - 1
        price = request.POST['price']
    product = get_object_or_404(Product, id=id)
    cart.add(product=product, quantity=number,price=price, update_quantity=True)
    return redirect('cart')