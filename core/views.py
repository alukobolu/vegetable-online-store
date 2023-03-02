from django.shortcuts import render, get_object_or_404,redirect
from django.views.generic.base import TemplateView
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from .models import Product,Sold
from .cart import Cart
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.views import View
# Create your views here.
from django.contrib.auth.views import LoginView
from django.contrib.auth import login, logout
from django.shortcuts import resolve_url
from django.views import View
from django.shortcuts import redirect

from .forms import LoginForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User

# User login view
class UserLoginView(LoginView):
    authentication_form = LoginForm
    form_class = LoginForm
    redirect_authenticated_user = False
    template_name = 'login.html'

    def get_success_url(self):
        url = self.get_redirect_url()
        return url or resolve_url('/')

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super(UserLoginView, self).form_valid(form)


# Logout view
class LogoutView(View):

    def get(self, request):
        logout(request)
        return redirect('/')

@method_decorator(login_required(login_url='/login/'), name='dispatch')
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

    def get_context_data(self, *args, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        context['user'] = User.objects.all()
        return context

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

class Items:
    def __init__(self,request,id):
        self.cart = Cart(request)
        self.product = get_object_or_404(Product, id=id)
        self.request = request

    def act(self):
        raise NotImplementedError("There is no act for this !!!")

class CartAdd(Items):
    def act(self):
        self.cart.add(product=self.product, quantity=1, update_quantity=False)

class CartRemove(Items):
    def act(self):
        self.cart.remove(self.product)

class CartUpdate(Items):
    def act(self):
        if self.request.POST['submit'] == 'add':
            number = int(self.request.POST['number']) + 1
        else:
            number = int(self.request.POST['number']) - 1
        price = self.request.POST['price']
        self.cart.add(product=self.product, quantity=number,price=price, update_quantity=True)

def cart_actions(action):
    action.act()

# Add to cart views
def cart_add(request, id):
    action = CartAdd(request, id)
    cart_actions(action)
    messages.success(request, f'Item has been added to cart.')
    return redirect('home')


# Remove Shopping Cart views
def cart_remove(request, id):
    action = CartRemove(request,id)
    cart_actions(action)
    return redirect('cart')


# update Shopping Cart views
@require_POST
def cart_updated(request, id):
    action = CartUpdate(request,id)
    cart_actions(action)
    return redirect('cart')